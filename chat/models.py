# -*- encoding: UTF-8 -*-
'''
Models for jchat application.

Let's try to make this as modular as possible, no strings attached

THIS IMPLEMENTATION HAS A TERRIBLE PROBLEM, NO VALIDATION IS DONE WETHER THE USER CAN OR NOT SAY SOMETHING HERE, SO 'GHOST' USERS COULD BE SENDING MESSAGES TO A CHAT ROOM...
THE OPTIMAL SOLUTION IS TO BIND THE CHAT ROOM WITH THE DIFFERENT OBJECTS THAT CAN USE IT, THAT IS, CREATE A FK FROM THE OBJECTS TO THE CHATROOM AND USE THE OBJECT ITSELF AS A VALIDATOR AND GATEWAY TO THE CHATROOM.
IN OTHER WAYS... IMPLEMENT A MODEL FOR CONNECTED USERS ASAP (I accept suggestions)

For more hardcore uses... a dedicated and specialized application should be better:
@see: http://en.wikipedia.org/wiki/Comet_(programming)

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType, ContentTypeManager 
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import datetime
from django.contrib import admin




class RoomManager(models.Manager):
    '''Custom model manager for rooms, this is used for "table-level" operations.
    All methods defined here can be invoked through the Room.objects class.
    @see: http://docs.djangoproject.com/en/1.0/topics/db/managers/#topics-db-managers
    Also see GenericTypes from the contenttypes django app!
    @see: http://docs.djangoproject.com/en/1.0/ref/contrib/contenttypes/''' 
    def create(self, object):
        '''Creates a new chat room and registers it to the calling object'''
        r = self.model(content_object=object)
        r.save()
        return r
        
    def get_for_object(self, object):
        '''Try to get a room related to the object passed.'''
        return self.get(content_type=ContentType.objects.get_for_model(object), object_id=object.pk)

    def get_or_create(self, object):
        '''Save us from the hassle of validating the return value of get_for_object and create a room if none exists'''
        try:
            return self.get_for_object(object)
        except Room.DoesNotExist:
            return self.create(object)

class Room(models.Model):
    '''Representation of a generic chat room'''
    content_type = models.ForeignKey(ContentType, blank=True, null=True) # to what kind of object is this related
    object_id = models.PositiveIntegerField(blank=True, null=True) # to which instace of the aforementioned object is this related
    content_object = GenericForeignKey('content_type','object_id') # use both up, USE THIS WHEN INSTANCING THE MODEL
    created = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    createdBy = models.CharField(blank=True,max_length=50,  default=False)
    dUsername = models.CharField(blank=True,max_length=50,  default=False)
    dtelno = models.CharField(null=True,max_length=50,  default=False)
    payment = models.CharField(null=True,max_length=50,  default=False)
    objects = RoomManager() # custom manager
    
    def __add_message(self, type, sender, message=None):
        '''Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m
    
    def say(self, sender, message):
        '''Say something in to the chat room'''
        return self.__add_message('m', sender, message)
    
    def join(self, user):
        '''A user has joined'''
        return self.__add_message('j', user)
    
    def leave(self, user):
        '''A user has leaved'''
        return self.__add_message('l', user)
    
    def messages(self, after_pk=None, after_date=None):
        '''List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')
    
    def last_message_id(self):
        '''Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0
    
    def __unicode__(self):
        return 'Chat for %s %d' % (self.content_type, self.object_id)
    
    class Meta:
        unique_together = (("content_type", "object_id"),)


MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)


class Message(models.Model):
    '''A message that belongs to a chat room'''
    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        '''Each message type has a special representation, return that representation.
        This will also be translator AKA i18l friendly.''' 
        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        if self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message


class Register(models.Model):

    user = models.OneToOneField(User , default=False)
    fname = models.CharField(blank=True, max_length=20,  default=False)
    sname = models.CharField(blank=True, max_length=30,  default=False)
    page = models.IntegerField(blank=True)
    gender = models.CharField(blank=True, max_length=30,  default=False)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    username = models.CharField(blank=True, max_length=20,default=False)
    password= models.CharField(max_length=30)
    email = models.CharField(blank=True,max_length=50,  default=False)
    street = models.CharField(blank=True,max_length=50,  default=False)
    city = models.CharField(blank=True,max_length=20, default=False)
    state = models.CharField(blank=True,max_length=20,  default=False)
    role2 = models.CharField(max_length=20, default=False)
    specialty = models.CharField(max_length=20, default=False)
    access_right= models.CharField(max_length=30,default=False)
    account_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_names(self):
        '''
        Return a users phonenumber
        '''
        text = '%s %s' % (self.fname, self.lname)
        try:
            text = text.encode('utf-8')
        except UnicodeEncodeError:
            pass
        return text

    def __unicode__(self):
        return self.username



class Illness(models.Model):
    added = models.DateTimeField(auto_now=True)
    email = models.CharField(blank=False, max_length=40)
    pname = models.CharField(blank=False, max_length=50)
    sname = models.CharField(blank=False, max_length=50)
    gender = models.CharField(blank=False, max_length=30) # gender is the payment Id
    illness = models.CharField(blank=False, max_length=700)  
    comp_signs =  models.CharField(blank=False, max_length=700) 
    kin = models.CharField(blank=False, max_length=30)
    kintelno = models.CharField(blank=False, max_length=20)
    username = models.CharField(blank=False, max_length=20)
    page = models.IntegerField(blank=False)
    amb =  models.CharField(blank=False,max_length=5,  default=False)
    amt = models.CharField(blank=False,max_length=5,  default=False)
    doctorusername = models.CharField(blank=False, max_length=20)
    location = models.CharField(blank=False, max_length=700)
    when  =  models.DateTimeField(default=datetime.now, blank=True)
    dtelno = models.CharField(blank=True, max_length=20)
    dname = models.CharField(blank=False, max_length=40)
    demail = models.CharField(blank=False, max_length=40)
    consultation_success = models.BooleanField(default=False)

    def get_names(self):
        '''
        Return a users phonenumber
        '''
        text = '%s %s' % (self.pname, self.sname)
        try:
            text = text.encode('utf-8')
        except UnicodeEncodeError:
            pass
        return text
    
   
   






class Document(models.Model):
    """Dummy document model, just for testing use"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)




class Ambulance(models.Model):
    '''store login data'''
    amb_time = models.DateTimeField(auto_now_add=True)
    area = models.CharField(blank=True,max_length=50,  default=False)
    city = models.CharField(blank=True,max_length=50,  default=False)
    phone = models.CharField(blank=True, max_length=20,  default=False)







class Orderdrugs(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    area = models.CharField(blank=True,max_length=50,  default=False)
    city = models.CharField(blank=True,max_length=50,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)
    when = models.DateTimeField(auto_now_add=True)
    staff_no = models.CharField(blank=True,max_length=70,  default=False)
    staff_name = models.CharField(blank=True,max_length=70,  default=False)


class Labtests(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    area = models.CharField(blank=True,max_length=50,  default=False)
    city = models.CharField(blank=True,max_length=50,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)
    when = models.DateTimeField(auto_now_add=True)
    staff_no = models.CharField(blank=True,max_length=70,  default=False)
    staff_name = models.CharField(blank=True,max_length=70,  default=False)








class Contact(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    email = models.CharField(blank=True,max_length=50,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)








class ConsultPayment(models.Model):

    # user = models.OneToOneField(User)
    p_telno = models.CharField(blank=True, max_length=20,  default=False)
    our_telno = models.CharField(blank=True, max_length=20,  default=False)
    doctor = models.CharField(blank=True,max_length=50,  default=False)
    patient = models.CharField(blank=True,max_length=50,  default=False)
    pay_time = models.DateTimeField(auto_now_add=True)
    cons_amount = models.IntegerField(blank=False)