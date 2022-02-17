window.onload=function(){
    var a = document.getElementsByClassName('pp');
    var cp = document.getElementById('cp');
    for(var i=0;i<a.length;i++){
        // console.log(a[i])
        // a[i].addEventListener('click',show1,false);
        (function(i){
            a[i].onclick = function() {
                show1(i)
            }
        })(i);
        
    }
    function show1(n){
        var k = 1;
        if (n ==1) {
            k = 0
        }
        // console.log(n)
        // console.log(a[n])
        // console.log(a[n].classList)
        if (a[n].classList.contains('dp')){
            a[n].classList.remove('dp')
            a[n].classList.add('cp')
            a[k].classList.remove('cp')
            a[k].classList.add('dp')
            cp.value = n;
        }
    }
    // alert(1)
    // var b = document.getElementById("search")
    // b.onsubmit=function(){
    //     console.log(b.name)
    //     for (let i=0;i<b.length;i++) {
    //         console.log(b.elements[i])
    //     }
    // }
}