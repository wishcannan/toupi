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
    function getnovelitem(){
        var a = localStorage.getItem('novelitem')
        if(a != null){
            a = a.split(',')
            return a
        }
        return []
    }
    function getchapter(l){
        for(var i = 0;i<l.length;i++){
            var v = localStorage.getItem('charpter'+l[i])
            if(a != null){
                l[i] = l[i]+'_'+v
            }
        }
        return l
    }
    function appendtable(rt){
        var $table = $('#chuangyixuanshou')
        for(var i = 0;i < rt.length;i++){
            var $tr = $('<tr></tr>')
            var $td1 = $('<td></td>')
            var $td2 = $('<td></td>')
            var $a1 = $('<a target="_blank"></a>')
            $a1.attr('href','/jianjie/' + rt[i].id)
            $a1.text(rt[i].name)
            $td1.append($a1)
            var $a2 = $('<a target="_blank"></a>')
            $a2.attr('href','/novel/' + rt[i].id+'/'+rt[i].cid)
            $a2.text(rt[i].cname)
            $td2.append($a2)
            $tr.append($td1)
            $tr.append($td2)
            $table.append($tr)
        }
        // $table.append('<tr><td></td></tr>')
    }
    var l = getchapter(getnovelitem())
    $.get(
        '/getnovelchaptername',{
            'data':JSON.stringify(l)
        },function(rt){
            appendtable(rt)
        }
    )
}