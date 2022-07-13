option_list=[document.getElementById('option1'), document.getElementById('option2'), document.getElementById('option3'), document.getElementById('option4')];
content_list=[document.getElementById('content1'), document.getElementById('content2'), document.getElementById('content3'), document.getElementById('content4')];


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


function enabled_admin_buttons(enabled){
    var blockeds = document.querySelectorAll(".blocked_admin_buttons");
    admin_validation= document.getElementById('admin_validation');
    admin_validated= document.getElementById('admin_validated');
    if (enabled == 1){
        admin_validation.style.display= 'none';
        admin_validated.style.display= 'block';
        for (i=0; i<blockeds.length; i++){
            blockeds[i].disabled= false;
            blockeds[i].style.textDecoration= "none";
        }
    }
    else {
        admin_validation.style.display= 'block';
        admin_validated.style.display= 'none';
        for (i=0; i<blockeds.length; i++){
            blockeds[i].disabled= true;
            blockeds[i].style.textDecoration= "line-through";
        }
    }
};

function view_mod_data(name, index){
    div= document.getElementById('empl_mod_data');
    p= document.getElementById('empl_data')
    if (div.style.display== 'none'){
        div.style.display='block';
        empl_data.innerHTML= 'Modificar Datos del Empleado: '+name;
        document.getElementById('employee_id').value= index;
    }
    else {
        div.style.display='none';
    }
}

function sub_id_validate(list){
    list= list.split(',), (');
    subscriber_id= document.getElementById('subscriber_id');
    button= document.getElementById('ticket_gen');
    str_id= String(subscriber_id.value);
    console.log(subscriber_id.value);
    for (let i=0; i<list.length; i++){
        if ( (list[i].includes(str_id) && str_id.length==4) || subscriber_id.value==''){
            console.log(list[i]);
            button.disabled= false;
            return;
        }
        button.disabled= true;
    }
}


function ExportToExcel(id_table, type, fn, dl) {
    var elt = document.getElementById(id_table);
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    return dl ?
      XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
      XLSX.writeFile(wb, fn || (id_table + '.' + (type || 'xlsx')));
}
