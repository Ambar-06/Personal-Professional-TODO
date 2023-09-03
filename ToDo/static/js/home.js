// my-script.js
function onhoverImg(imgElement) {
document.getElementById('togglebinImg').addEventListener('mouseenter', function() {
    let imgpath = document.getElementById('togglebinImg').src;
    let img_array = imgpath.split("/");
    let img = img_array[img_array.length - 1]
    if(img === "bin.png"){
        let newimgpath = imgpath.replace('bin.png', 'binopen.png')
        imgpath = newimgpath
        document.getElementById('togglebinImg').src = imgpath;
        console.log(imgpath)
                console.log('Hovered')
            }
    else{
        let newimgpath = imgpath.replace('binopen.png', 'bin.png')
        imgpath = newimgpath
        document.getElementById('togglebinImg').src = imgpath;
        console.log(imgpath)
        console.log('mouse away')
    }
})

    document.getElementById('togglebinImg').addEventListener('mouseleave', function() {
        let imgpath = document.getElementById('togglebinImg').src;
        let img_array = imgpath.split("/");
        let img = img_array[img_array.length - 1]
        if(img === "bin.png"){
            let newimgpath = imgpath.replace('bin.png', 'binopen.png')
            imgpath = newimgpath
            document.getElementById('togglebinImg').src = imgpath;
            console.log(imgpath)
                    console.log('Hovered')
                }
        else{
            let newimgpath = imgpath.replace('binopen.png', 'bin.png')
            imgpath = newimgpath
            document.getElementById('togglebinImg').src = imgpath;
            console.log(imgpath)
            console.log('mouse away')
        }
})};
