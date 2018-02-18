document.getElementById("header").innerHTML = "Order Drugs";

        function addFields(){
            // Number of inputs to create
            var number = document.getElementById("member").value;
            // Container <div> where dynamic content will be placed
            var container = document.getElementById("container");
            // Clear previous contents of the container

            var back = "Back";
            var divColor = "white";

            var leftDiv = document.createElement("div"); //Create left div
                    leftDiv.id = "left"; //Assign div id
                    leftDiv.setAttribute("style", "position:absolute; top:0;left:0;color: rgb(155, 45,82);text-decoration: underline;"); //Set div attributes
                    leftDiv.style.background =  divColor;
                    a = document.createElement('a');
                    a.setAttribute('href', '/');
                    a.appendChild(document.createTextNode(back + ' '));
                    leftDiv.appendChild(a); // Add name to left div

                    document.body.appendChild(leftDiv);
                    container.appendChild(document.createElement("br"));
                    container.appendChild(document.createElement("br"));
                              

            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
            for (i=0;i<number;i++){
                // Append a node with a random text
                container.appendChild(document.createTextNode("Drug " + (i+1)));
                // Create an <input> element, set its type and name attributes
                var input = document.createElement("input");
                input.type = "text";
                input.name = "member";
                container.appendChild(input);

                container.appendChild(document.createTextNode("Amount " + (i+1)));

                var input2 = document.createElement("input");
                input2.type = "text";
                input2.name = "qty";
                container.appendChild(input2);

                // Append a line break 
                container.appendChild(document.createElement("br"));
                container.appendChild(document.createElement("br"));
            }
            container.appendChild(document.createTextNode("Phone: " ));

            var input_phone = document.createElement("input");
                input_phone.type  = "text";
                input_phone.name = "telno";
                container.appendChild(input_phone);

           container.appendChild(document.createElement("br"));
           container.appendChild(document.createElement("br"));
           container.appendChild(document.createTextNode("City: " ));
           //Create array of options to be added
      var array = ["--Select City--","Kampala"];

      //Create and append select list
      var selectList = document.createElement("select");
      selectList.id = "mySelect";
      container.appendChild(selectList);
      selectList.name = "city";
      container.appendChild(selectList);

      //Create and append the options
      for (var i = 0; i < array.length; i++) {
          var option = document.createElement("option");
          option.value = array[i];
          option.text = array[i];
          selectList.appendChild(option);
      }


           
           container.appendChild(document.createElement("br"));
           container.appendChild(document.createElement("br"));
           container.appendChild(document.createTextNode("Area: " ));
      //Create array of options to be added
      var array = ["--Select Area--", "Banda","Bbunga","Bugolobi","Bukasa","Bukoto","Bulangi","Bukesa","Bulange","Bulwa","Buziga","Center Business District","Ggaba","Kabalagala","Kalerwe","Kamwokya","Kansanga","Kasubi","Katwe","Kasubi","Kawaala","Kawuku","Kikaaya","Kasubi","Kikoni","Kinawataka","Kireka","Kisasi","Kisementi","Kasubi","Kitintale","Kiwaatule","Kiwafu","Kololo","Kulambiro","Kiwaatule","Kamwokya","Kansanga","Kanyanya","Kasubi","Kawaala","Kibuli","Kibuye","Kigowa","Kikaaya","Kyambogo","Kyanja","Kyebando","Lubowa","Lugogo","Luwafu","Luzira","Makindye","Mbuya","Mengo","Mpererwe","Mulago","Munyonyo","Mutungo","Muyenga","Namugongo","Naalya","Rubaga","Najjanankumbi","Najjera 1","Nakawa","Nakulabye","Namirembe","Ndeeba","Ntinda","Ntinda Industrial Area","Wandegeya","Nakivubo","Zana","zzz_testnororder","Ndeeba"];

      //Create and append select list
      var selectList = document.createElement("select");
      selectList.id = "mySelect";
      container.appendChild(selectList);
      selectList.name = "area";
      container.appendChild(selectList);

      //Create and append the options
      for (var i = 0; i < array.length; i++) {
          var option = document.createElement("option");
          option.value = array[i];
          option.text = array[i];
          selectList.appendChild(option);
      }
      container.appendChild(document.createElement("br"));

      var input_submit = document.createElement("input");
      input_submit.type  = "submit";
      input_submit.name = "submit";
      input_submit.id = "submit";
      container.appendChild(input_submit);
         



        }