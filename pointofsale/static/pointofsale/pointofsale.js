$(document).ready(function() {
    // Assign id's to the drink fields automatically (Django doesn't do this for some reason)
    i = 0;
    $('#drinks div.drink input').each(function() {
        this.id = "drink_" + i++;
    });
    
    // Assign ids to the account fields automagically
    j = 0;
    $('#accounts input').each(function() {
        this.id = "account_" + j++;
    });
    
    // When the user clicks anywhere in the table the right radio button should be selected
    $('#accounts tr').click(function() {
        $(this).find('input:radio').prop('checked', true);
        $(this).find('input:radio').change();
    });
    
    $("#accounts input:radio").css("border", "1px solid black");
    
    $("#accounts input:radio").change(function() {
        $("#accounts tr").removeClass("selected");
        $(this).parents("tr").addClass("selected");
    });
});

