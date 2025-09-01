const elementToCopy = document.querySelector('div[data-test="hdp-for-sale-page-content"]');

if (elementToCopy) {
    const elementHTML = elementToCopy.outerHTML;

    // This is a more robust way to copy, to avoid "NotAllowedError"
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = elementHTML;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    tempTextArea.setSelectionRange(0, 99999); 
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);

    console.log('Element HTML copied to clipboard!');
} else {
    console.warn('Element with data-test="hdp-for-sale-page-content" not found.');
}