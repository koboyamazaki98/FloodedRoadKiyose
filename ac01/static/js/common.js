function commonPageLoad(sender){
    $('#spnOpTime').text($('#hdnOpTime').val());
}


function commonFormSubmit(sender, form){
    $("#hdnFunctionCd").val(sender.value);
    form.submit();
}
