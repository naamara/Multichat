from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User 

from .models import Room, Message


from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404

from chat.models import Document, Orderdrugs,Labtests,Contact

from chat.utils import All_doctors, doctor_users
from django.contrib.auth.models import User
from chat.models import Register,Illness
from django.contrib.auth import authenticate,login as auth_login
from django.shortcuts import render
from multichat.settings import PATIENT, DOCTOR ,ADMIN
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from chat.forms import CreateAdminUserForm
from AfricasTalkingGateway.server import SendSms
from chat.check_area import *
from chat.check_areas import *
from django.contrib import messages


@csrf_exempt
@login_required
def send(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.say(request.user, p['message'])
    return HttpResponse('')

@csrf_exempt
@login_required
def sync(request):
    '''Return last message id

    EXPECTS the following POST parameters:
    id
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None):
        raise Http404

    r = Room.objects.get(id=post['id'])
    
    lmid = r.last_message_id()    
    
    return HttpResponse(jsonify({'last_message_id':lmid}))

@csrf_exempt
@login_required
def receive(request):
    '''
    Returned serialized data
    
    EXPECTS the following POST parameters:
    id
    offset
    
    This could be useful:
    @see: http://www.djangosnippets.org/snippets/622/
    '''
    if request.method != 'POST':
        raise Http404
    post = request.POST

    if not post.get('id', None) or not post.get('offset', None):
        raise Http404
    
    try:
        room_id = int(post['id'])
    except:
        raise Http404

    try:
        offset = int(post['offset'])
    except:
        offset = 0
    
    r = Room.objects.get(id=room_id)

    m = r.messages(offset)

    
    return HttpResponse(jsonify(m, ['id','author','message','type']))


@csrf_exempt
@login_required
def join(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.join(request.user)
    return HttpResponse('')


@csrf_exempt
@login_required
def leave(request):
    '''
    Expects the following POST parameters:
    chat_room_id
    message
    '''
    p = request.POST
    r = Room.objects.get(id=int(p['chat_room_id']))
    r.leave(request.user)
    return HttpResponse('')


@csrf_exempt
@login_required
def test(request):
    '''Test the chat application'''
    
    u = User.objects.get(id=1) # always attach to first user id
    r = Room.objects.get_or_create(u)

    return render_to_response('chat/chat.html', {'js': ['/media/js/mg/chat.js'], 'chat_id':r.pk}, context_instance=RequestContext(request))


def jsonify(object, fields=None, to_dict=False):
    '''Simple convert model to json'''
    try:
        import json
    except:
        import django.utils.simplejson as json
 
    out = []
    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object
    if to_dict:
        return out
    else:
        return json.dumps(out)






def landing(request):
    """Index page, force login here"""
    context = RequestContext(request)
    return render_to_response('index_pat.html', {'documents':Document.objects.all()})


def simple(request, id):
    """Simple chat room demo, it is not attached to any other models"""
    # get the chat instance that was created by the fixture, pass the id to the template and you're done!
    dtelno = Room.objects.get(id=id).dtelno
    comment = Room.objects.get(id=id).comment
    createdBy = Room.objects.get(id=id).createdBy

    print "Doctor Phone number", dtelno

    

    return render_to_response('simple.html', {'chat_id':Room.objects.get(id=id).id}) 



def simple2(request, id):
    """Simple chat room demo, it is not attached to any other models"""
    # get the chat instance that was created by the fixture, pass the id to the template and you're done!
    dtelno = Room.objects.get(id=id).dtelno
    comment = Room.objects.get(id=id).comment
    createdBy = Room.objects.get(id=id).createdBy

    print "Doctor Phone number", dtelno

    return render_to_response('simple.html', {'chat_id':Room.objects.get(id=id).id}) 





@login_required
def complex(request, id):
    """Complex chat room demo, it uses the RoomManager to get the instance associated to the object"""
    
    # get the document requested by the url
    doc = get_object_or_404(Document, id=id)
    # get *or create* a chat room attached to this document
    room = Room.objects.get_or_create(doc)
    
    return render_to_response('complex.html', {'document':doc, 'chat_id':room.id})  





@csrf_exempt
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    doctor_users = None 
    try: 

    # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
            # Attempt to grab information from the raw form information.
            # Note that we make use of both UserForm and UserProfileForm.
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            password = request.POST['password']
            role = request.POST['role']

            doctor_users = All_doctors(doctor_users)

            user = User(username=username, email=email)
            user.save()
            user.set_password(password)
            user.save()
            
          
            rg = Register(user=user, username=username, password=password, email=email, page='0',role2=role)
            rg.save()
            print 'Password %s' % rg.password
            print 'Password %s' % rg.username
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserPro2
            user = authenticate(username=rg.username, password=rg.password)
            if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        
                        return render(request, "pat_chat.html", {'doctor_users':doctor_users,'username':rg.username
        
            })
            
                

            return render_to_response('index_pat.html',{'registered': registered}, context)
            registered = True
        
    except Exception, e:
        pass
        return render_to_response('index_pat.html',{'registered': registered}, context)

    print "OOOK"
    return render_to_response('register.html',{'registered': registered}, context)






def illness(request):
    
    context = RequestContext(request)
    post_values = {}
    push_notif = {}
    AfricasTalk = None
    AfricasTalk  = AfricasTalk
    doctor_sms_data = {}
    dp_room = None

    password = None
    dname = None
    pdiog = None
    dtelno = None
    doctor_users = None
    doctor_users = All_doctors(doctor_users)
    us = None
    gender = None
    if request.POST:
        post_values = request.POST.copy()
        
        comp_signs = request.POST['comp_signs']
        illness = request.POST['illness']
        amb = request.POST['amb']
        gender = request.POST['gender']
        username = request.POST['username']
        password = request.POST['password']
        city = request.POST['city']
        state = request.POST['state']
        role= request.POST['role']
        ptelno = request.POST['telno']
        dname = request.POST['dname']


        try:
            check_doctor = Register.objects.get(username=dname)
            dtelno = check_doctor.telno
        except Exception,e:

            print 'Doctor Does not exist', e

        print "Doctor name %s " % (dname)

        print "Doctor Phonenumber %s " % (dtelno)

        ill_det=Illness(gender=gender,comp_signs=comp_signs, dtelno=dtelno,illness=illness, kintelno=ptelno,page=0,username=username, dname=dname,doctorusername=dname,amt=8000)
        ill_det.save()
        print 'Patient User name %s ' % username

        comp_signs = request.POST['comp_signs']
        dpassword = '0754307471'
        dusername = '0754307471'


                
        try:
            dp_room=Room.objects.get(createdBy=dname,dUsername=username)  
        except Exception,e:
            dp_room=Room(createdBy=username,dUsername=dname, dtelno=dtelno, comment=illness)
            dp_room.save()
            print "OOOOOOK"


        print "Doctor Username", dp_room.dUsername


        # send patient consultation  successs    
        push_notif['registration_id'] = "61464121334"
        push_notif['message_title'] = "Medical Consulation"
        push_notif['message_body'] = comp_signs
        push_notif['api_key'] = "AIzaSyBdlecKJpqsOlgXah9-Bd-rGoG7m_hewWI"
        
        # send_illness_sms_notification(request,
  #            msg)
        # send sms
        doctor_sms_data['receiver_number'] = dtelno
        # send sms to doctor so that patient can chat with him or her   SendSms(doct_data)
        #SendSms(doctor_sms_data)
        # illdecsuccess
        return render_to_response('index.html', { 'password':password,'gender':gender,   'dp_room':dp_room}, context)


    else:
        return render_to_response('index_pat.html', { 'password':password,'gender':gender,   'dp_room':dp_room}, context)






@csrf_exempt
def user_login(request):
    # Like before, obtain the context for the user's hrequest.
    context = RequestContext(request)
    msg = ''
    response = None
    log = False
    convmem = ''
    phonedoctor = ''
    data = {}
    password = None
    username = None
    pay_status = None
    staf=False
    auth_error = False
    dname = None
    check_user = None
    dp_room1 = None
    dp_room = None
    check_doct = None
    dtelno=None
    doctor_users =None
    doctor_users = All_doctors(doctor_users)
    doctor_sms_data = {}

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        password = request.POST.get('password', None)
        username = request.POST.get('username', None)
        


        try:
            check_user = Register.objects.get(password=password, username=username)

        except Register.DoesNotExist:
            listing = None
           
            auth_error = True
            return render_to_response('index_pat.html', {'log':log, 'auth_error':auth_error}, context)


        
        if check_user.role2 == PATIENT:
       
            try:
                check_doct = Illness.objects.get(username=username)
                dtelno = check_doct.dtelno
            except Exception, e:
                pass


            print 'Receiver No', dtelno
                    

        
            doctor_sms_data['receiver_number'] = dtelno
            print 'Receiver No', doctor_sms_data['receiver_number']
            # send sms to doctor so that patient can chat with him or her   SendSms(doct_data)
            #SendSms(doctor_sms_data)

            try:
                dp_room=Room.objects.filter(createdBy=username) 
                for dp_room in dp_room:
                    print "Doct name ", dp_room.dUsername 
            except Exception,e:
                dp_room1=Room.objects.get(createdBy=username)
                print "Doct name 1", dp_room1.dUsername

            print "Username", username
            print "Password", password

            
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if dp_room:
                        return render(request, "index.html", {'dp_room':dp_room,'dp_room1':dp_room1,'username':username
        })

                    
                    return render(request, "pat_chat.html", {'doctor_users':doctor_users, 'dp_room':dp_room,'dp_room1':dp_room1,'username':username

        })
        
    

        elif check_user.role2 == DOCTOR:
                try:
                    dp_room=Room.objects.filter(dUsername=username)  
                except Exception,e:
                    dp_room=Room.objects.get(dUsername=username)

                print "Username", username
                print "Password", password


                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                        print "Username 1", username
                        print "Password 1", password
                        
                        return render(request, "doct_chat.html", {'dp_room':dp_room,'username':username
        
            })

        elif check_user.role2 == ADMIN:
                try:
                    dp_room=Room.objects.filter(dUsername=username)  
                except Exception,e:
                    dp_room=Room.objects.get(dUsername=username)

                print "Username", username
                print "Password", password


                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                        print "Username 1", username
                        print "Password 1", password
                        
                        return render(request, "index_admin.html", {'dp_room':dp_room,'username':username
        
            })


    return render(request, "index_pat.html", {
        
            })





def homeadmin(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    
    # Render that in the index template
    return render(request, "admin_login.html", {
       
    })




def create_stuff_user(request, is_customer_care=False):
    '''create an admin user'''
    reg_success = False
    exist = False
    form = CreateAdminUserForm()
    if request.POST:
        print "Username", request.POST['username']
        user = User(username=request.POST['username'])
        user.set_password(request.POST['password'])
        user.save()
        user.is_staff = True
        user.save()

        reg = Register(user=user,telno=request.POST['telno'],
            username=request.POST['username'],password=request.POST['password'],email=request.POST['email'],role2=request.POST['role'],page=0)
        try:
            check_existance = Register.objects.get(username=username)
            if check_existance:
                exist = True
                return render(request, "create_stuff_user.html", {'form': form, 'super_admin':super_admin, 'reg_success':reg_success
    
        })
        except Exception,e:
            pass

        reg.save()
        reg_success = True
  
            
    super_admin = True

    return render(request, "create_stuff_user.html", {'form': form, 'super_admin':super_admin, 'reg_success':reg_success
        
            })






def about(request):
    # Like before, obtain the context for the user's hrequest.
    context = RequestContext(request)
    
    return render_to_response('about.html', {}, context)


def whyus(request):
    # Like before, obtain the context for the user's hrequest.
    context = RequestContext(request)
    
    return render_to_response('whyus.html', {}, context)


def contact(request):
    # Like before, obtain the context for the user's hrequest.
    context = RequestContext(request)
    post_values = ''
        

    
    return render_to_response('contactus.html', {}, context)

def our_team(request):
    # Like before, obtain the context for the user's hrequest.
    context = RequestContext(request)
    
    return render_to_response('ourteam.html', {}, context)




def  how_it_works(request):
    context = RequestContext(request)

    return render_to_response(
    'how_it_works.html',
    {},
    context)



@csrf_exempt
def labtests(request):
    
    response = False
    staff_no = None
    staff_name  = None
    Check_area = None

    order_drug = True

    post_values = {}
    context = RequestContext(request)

    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        location = post_values['city']
        msg = post_values['msg']
        print "Message %s " %  msg


      
        staff_no, staff_name = test_staff(location, staff_no, staff_name)

        
        cont=Labtests(telno=telno,city=location, msg=msg, staff_no=staff_no, staff_name=staff_name)
        cont.save()
        response = True

        if cont:
            messages.success(request, "You have been Successfully ordered for Lab tests")
            
            
        else:
            messages.success(request, "Error occured while ordering for Lab tests")
          


    return render_to_response('labtests.html', {'order_drug':order_drug}, context)



@csrf_exempt
def orderdrugs(request):
    
    response = False
    post_values = {}
    context = RequestContext(request)
    Check_area = None

    staff_no = " "
    staff_name  = " "
    labtest = True


    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        location = post_values['city']
        area = post_values['area']
        msg = post_values['msg']
        print "Message %s " %  msg

  
        staff_no, staff_name = drug_staff(location, staff_no, staff_name)
        
        cont=Orderdrugs(telno=telno,city=location, area=area, msg=msg, staff_no=staff_no, staff_name=staff_name)
        cont.save()
        response = True

        if cont:
            messages.success(request, "Your have been Successfully ordered for drugs")
            
            
        else:
            messages.success(request, "Error occured while ordering for drugs")
          


    return render_to_response('orderdrugs.html', {'labtest':labtest}, context)





@csrf_exempt
def addcontact(request):
  
    response = False
    post_values = {}
    context = RequestContext(request)

    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        email = post_values['email']
        name = post_values['name']
        msg = post_values['msg']
        print "Message %s " %  msg
        
        cont=Contact(telno=telno,email=email, msg=msg)
        cont.save()
        response = True

        if cont:
            messages.success(request, "Your contact details have been Successfully added")
            
            
        else:
            messages.success(request, "Error occured while adding your contact details")
          


    return render_to_response('contactus.html', {}, context)