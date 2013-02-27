
CKEDITOR.editorConfig = function( config )
{
    config.skin = 'v2';
    config.toolbar =
        [
            { name: 'document',    items : [ 'Source','-',,'DocProps','Preview','-'] },
            { name: 'clipboard',   items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
            { name: 'editing',     items : [ 'Find','Replace','-','SelectAll', ] },
            { name: 'tools',       items : [ 'Maximize', 'ShowBlocks' ] },
            '/',
            { name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','-','RemoveFormat' ] },
            { name: 'paragraph',   items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-'] },
           { name: 'styles',      items : ['Format','FontSize' ] },
            { name: 'links',       items : [ 'Link','Unlink','Anchor' ] }
           // { name: 'insert',      items : [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak' ] },
           // { name: 'colors',      items : [ 'TextColor','BGColor' ] },
            
        ];

};

