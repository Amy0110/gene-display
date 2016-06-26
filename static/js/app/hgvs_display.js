var request1 = $.ajax({
            type: "GET",
            url: "/hgvs_display1/",
            dataType: "json"
            });
            request1.done(function(data){
                var d=data;
                var trlist="";
                for (var i=0;i<d.length;i++){
                    text=d[i];
                    console.log(text);
                    var tdlist="";
                    for (var key in text){
                        tdlist += "<td>" + text[key] + "</td>";}
                    trlist += "<tr>" + tdlist + "</tr>";
                    }
                document.getElementById("info1").innerHTML = trlist;
                console.log(trlist);
            });
            request1.fail(function(jqXHR,textStatus){
                alert("Request failed: "+ textStatus);
            });
var request2 = $.ajax({
            type: "GET",
            url: "/hgvs_display2/",
            dataType: "json"
            });
            request2.done(function(data){
                var d=data;
                var trlist="";
                for (var i=0;i<d.length;i++){
                    text=d[i];
                    console.log(text);
                    var tdlist="";
                    for (var key in text){
                        tdlist += "<td>" + text[key] + "</td>";}
                    trlist += "<tr>" + tdlist + "</tr>";
                    }
                document.getElementById("info2").innerHTML = trlist;
                console.log(trlist);
            });
            request2.fail(function(jqXHR,textStatus){
                alert("Request failed: "+ textStatus);
            });

