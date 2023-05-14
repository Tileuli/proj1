var opts = [];
var nums = [];
var text = document.querySelector("#area");
var clear = document.querySelector("#clear");
var dlt = document.querySelector("#dlt");
var dot = document.querySelector("#dot");
var eq = document.querySelector("#eq");
var sc1 = document.querySelector("#sc1");
var sc2 = document.querySelector("#sc2");
var arr = ["+", "-", "*", "/"];

for(var i = 0; i <= 9; i++) {
    (function(i){
        num = "#num" + i;
        nums.push(document.querySelector(num));
        nums[i].addEventListener("click", function(){
            if(text.textContent == "Error") {
                text.textContent = "";
                return;
            }
            text.textContent += i;
        });
    }(i));
}

for(var i = 0; i <= 3; i++) {
    (function(i){
        btn_id = "#func" + i;
        btn = document.querySelector(btn_id);
        btn.addEventListener("click", function(){
            if(text.textContent.charAt(text.textContent.length-1)=="+" || text.textContent.charAt(text.textContent.length-1)=="-" ||
            text.textContent.charAt(text.textContent.length-1)=="/" || text.textContent.charAt(text.textContent.length-1)=="*") {
                text.textContent = text.textContent.substring(0,text.textContent.length-1);
            }
            if(text.textContent == "Error") {
                text.textContent = "";
                return;
            }
            text.textContent += arr[i];
        });
    })(i);
}

clear.addEventListener("click", function(){
    text.textContent = "";
});

dlt.addEventListener("click", function(){
    if(text.textContent == "Error") {
        text.textContent = "";
        return;
    }
    text.textContent = text.textContent.substring(0, text.textContent.length - 1);
});

dot.addEventListener("click", function(){
    if(text.textContent == "Error") {
        text.textContent = "";
        return;
    }
    text.textContent += ".";
});

sc1.addEventListener("click", function(){
    if(text.textContent == "Error") {
        text.textContent = "";
        return;
    }
    text.textContent += "(";
});

sc2.addEventListener("click", function(){
    if(text.textContent == "Error") {
        text.textContent = "";
        return;
    }
    text.textContent += ")";
});

eq.addEventListener("click", function(){
    if(text.textContent == "Error") {
        text.textContent = "";
        return;
    }
    try{
		text.textContent = eval(text.textContent);
	}
	catch(e){
	    text.textContent = "Error";
	}
});

