option1= document.getElementById('option1');
option2= document.getElementById('option2');
option3= document.getElementById('option3');
option4= document.getElementById('option4');
content1= document.getElementById('content1');
content2= document.getElementById('content2');
content3= document.getElementById('content3');
content4= document.getElementById('content4');
default_content= document.getElementById('default_content');

option1.onclick=()=>{
    default_content.style.display= 'none';
    option1.style.backgroundColor= 'white';
    content1.style.display= 'grid';
    option2.style.backgroundColor= 'green';
    content2.style.display= 'none';
    option3.style.backgroundColor= 'green';
    content3.style.display= 'none';
    option4.style.backgroundColor= 'green';
    content4.style.display= 'none';
}
option2.onclick=()=>{
    default_content.style.display= 'none';
    option2.style.backgroundColor= 'white';
    content2.style.display= 'grid';
    option1.style.backgroundColor= 'green';
    content1.style.display= 'none';
    option3.style.backgroundColor= 'green';
    content3.style.display= 'none';
    option4.style.backgroundColor= 'green';
    content4.style.display= 'none';
}
option3.onclick=()=>{
    default_content.style.display= 'none';
    option3.style.backgroundColor= 'white';
    content3.style.display= 'grid';
    option1.style.backgroundColor= 'green';
    content1.style.display= 'none';
    option2.style.backgroundColor= 'green';
    content2.style.display= 'none';
    option4.style.backgroundColor= 'green';
    content4.style.display= 'none';
}
option4.onclick=()=>{
    default_content.style.display= 'none';
    option4.style.backgroundColor= 'white';
    content4.style.display= 'grid';
    option2.style.backgroundColor= 'green';
    content2.style.display= 'none';
    option3.style.backgroundColor= 'green';
    content3.style.display= 'none';
    option1.style.backgroundColor= 'green';
    content1.style.display= 'none';
}