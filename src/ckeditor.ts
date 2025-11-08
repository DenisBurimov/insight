import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';
import Essentials from '@ckeditor/ckeditor5-essentials/src/essentials';
import Paragraph from '@ckeditor/ckeditor5-paragraph/src/paragraph';
import Bold from '@ckeditor/ckeditor5-basic-styles/src/bold';
import Italic from '@ckeditor/ckeditor5-basic-styles/src/italic';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline';
import Strikethrough from '@ckeditor/ckeditor5-basic-styles/src/strikethrough';
import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment';
import Font from '@ckeditor/ckeditor5-font/src/font';
import Undo from '@ckeditor/ckeditor5-undo/src/undo';
import List from '@ckeditor/ckeditor5-list/src/list';

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.editor').forEach(editorElement => {
    ClassicEditor.create(editorElement as HTMLElement, {
      plugins: [
        Essentials,
        Paragraph,
        Bold,
        Italic,
        Underline,
        Strikethrough,
        Alignment,
        Font,
        Undo,
        List,
      ],
      toolbar: [
        'bold',
        'italic',
        'underline',
        'strikethrough',
        '|',
        'alignment:left',
        'alignment:center',
        'alignment:right',
        'alignment:justify',
        '|',
        'fontSize',
        'fontFamily',
        'fontColor',
        'fontBackgroundColor',
        '|',
        'numberedList',
        'bulletedList',
        '|',
        'undo',
        'redo',
      ],
    })
      .then(editor => {
        console.log('Ckeditor was initialized', editor);
      })
      .catch(error => {
        console.error('Error initializing ckeditor:', error);
      });
  });
});
