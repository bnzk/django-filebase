if (typeof filebase_jquery_backup !== 'undefined') {
    // We made a backup of the original global jQuery before forcing it to our
    // yl.jQuery value. Now that select2 has been set up, we need to restore
    // our backup to its rightful place.
    jQuery = filebase_jquery_backup;
    $ = filebase_jquery_backup;
}