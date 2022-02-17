window.onload=function(){
    var a = document.getElementById('tjsq')
    a.onclick = function(){
        var b = window.location.pathname.split('/')
        var novellist = localStorage.getItem('novelitem')
        if(novellist != null){
            novellist = novellist.split(',')
        }else{
            novellist = Array()
        }
        var c = novellist.indexOf(b[2])
        if(c<0){
            novellist.push(b[2])
        }
        localStorage.setItem('novelitem',novellist)
        localStorage.setItem('charpter'+b[2],b[3])
    }
}