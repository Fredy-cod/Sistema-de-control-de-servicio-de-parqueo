option_list=[document.getElementById('option1'), document.getElementById('option2'), document.getElementById('option3'), document.getElementById('option4'), document.getElementById('option5')];
content_list=[document.getElementById('content1'), document.getElementById('content2'), document.getElementById('content3'), document.getElementById('content4'), document.getElementById('content5')];

option_list[0].onclick=()=>{
    for (let i=0; i<5; i++){
        if (i==0){
            option_list[0].style.backgroundColor= 'var(--content_color)';
            content_list[0].style.display= 'grid';
        }
        else {
            option_list[i].style.backgroundColor= 'var(--aside_color)';
            content_list[i].style.display= 'none';
        }
    }
};
option_list[1].onclick=()=>{
    for (let i=0; i<5; i++){
        if (i==1){
            option_list[1].style.backgroundColor= 'var(--content_color)';
            content_list[1].style.display= 'grid';
        }
        else {
            option_list[i].style.backgroundColor= 'var(--aside_color)';
            content_list[i].style.display= 'none';
        }
    }
};
option_list[2].onclick=()=>{
    for (let i=0; i<5; i++){
        if (i==2){
            option_list[2].style.backgroundColor= 'var(--content_color)';
            content_list[2].style.display= 'grid';
        }
        else {
            option_list[i].style.backgroundColor= 'var(--aside_color)';
            content_list[i].style.display= 'none';
        }
    }
};
option_list[3].onclick=()=>{
    for (let i=0; i<5; i++){
        if (i==3){
            option_list[3].style.backgroundColor= 'var(--content_color)';
            content_list[3].style.display= 'grid';
        }
        else {
            option_list[i].style.backgroundColor= 'var(--aside_color)';
            content_list[i].style.display= 'none';
        }
    }
};
option_list[4].onclick=()=>{
    for (let i=0; i<5; i++){
        if (i==4){
            option_list[4].style.backgroundColor= 'var(--content_color)';
            content_list[4].style.display= 'grid';
        }
        else {
            option_list[i].style.backgroundColor= 'var(--aside_color)';
            content_list[i].style.display= 'none';
        }
    }
};