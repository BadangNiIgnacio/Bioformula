$(document).ready(function(){
    $("#search-box").on('keyup', function(){
        let query = $(this).val();
        
        if (query.length > 0) {
            $.ajax({
                url: '/search-suggestions-pest',  // The URL for the AJAX request
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    let suggestionsBox = $("#suggestions-box");
                    suggestionsBox.empty();
                    if (data.suggestion.length > 0) {
                        suggestionsBox.show();
                        suggestionsBox.append('<div class="suggestion-item" style="border-bottom: 1px solid #ccc; padding-top: 1%; padding-bottom: 1%; padding-left: 1%; font-size: 12pt; text-align:center; color: green;">Ingredients</div>');
                        $.each(data.suggestion, function(index, item) {
                            suggestionsBox.append('<div class="suggestion-item" style="border-bottom: 1px solid #ccc; padding-top: 1%; padding-bottom: 1%; padding-left: 1%; font-size: 12pt; cursor: pointer;">' + item.description + '</div>');
                        });

                        if (data.pesticides.length > 0){
                            suggestionsBox.append('<div class="suggestion-item" style="border-bottom: 1px solid #ccc; padding-top: 1%; padding-bottom: 1%; padding-left: 1%; font-size: 12pt; text-align:center; color: green;">Pesticides</div>');
                            $.each(data.pesticides, function(index, item) {
                                suggestionsBox.append('<div class="suggestion-item" style="border-bottom: 1px solid #ccc; padding-top: 1%; padding-bottom: 1%; padding-left: 1%; font-size: 12pt; cursor: pointer;">' + item.name + '</div>');
                            });
                        }
                    } else {
                        suggestionsBox.hide();
                    }
                }
            });
        } else {
            $("#suggestions-box").hide();
        }
    });

    // Optional: Handle clicking on a suggestion
    $(document).on('click', '.suggestion-item', function(){
        $("#search-box").val($(this).text());
        $("#suggestions-box").hide();
    });
});