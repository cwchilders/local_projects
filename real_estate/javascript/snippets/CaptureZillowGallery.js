// This script captures the HTML of a specific element on a Zillow page and copies it to the clipboard.
const elementToCopy = document.querySelector('[class*="StyledVerticalMediaWall__StyledModalBody"]');

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
    console.warn('Element with class*="StyledVerticalMediaWall__StyledModalBody not found.');
}