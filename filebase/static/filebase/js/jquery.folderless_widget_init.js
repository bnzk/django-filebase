
(function($){
    // ready
    $(function() {

        $('.inline-group').each(function(index, inline) {
            if ($(inline).find("fieldset .filebase_raw_id_field").size()) {
                // found inline with filebase fields
                //console.log("found inline with filebase fields!");
                //console.log($(inline).attr("id"));
                $(inline).find(".add-row").click(add_row_handler);
            };
        });

        function add_row_handler(event) {
            // depends on html structure, bad. but...
            inline = $(event.currentTarget).parent();
            // f*** inlines ;
            to_enhance = inline.find(".last-related:not(.empty-form ) [data-widget=filebase_file]:not(.filebase_widget_initialized)");
            to_enhance.filebase_file_widget();
        }

        // add to all but empty-form (these are empty inlines that get duplicated)
        // console.log(filebase_jquery("div[data-widget=filebase_file]").not("[class*=__prefix__]"));
        $("div[data-widget=filebase_file]").not("[class*=__prefix__]").filebase_file_widget();

    });

})(filebase.jQuery);
