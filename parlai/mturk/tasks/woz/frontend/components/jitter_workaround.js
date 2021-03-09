function workaroundJitterBug() {
  try {
    // Parlai constantly refreshes the UI and recalculates the height of
    // the left pane component. On some devices, this can alternative between
    // 561px and 560px, resulting in an unpleasant jitter. The following code
    // adds a CSS rule which enforces 560px at all time.

    const workaroundCss = `div#right-top-pane {
        height: 560px !important;
    }`;

    const style = document.createElement("style");
    // WebKit hack :(
    style.appendChild(document.createTextNode(""));

    // Add the <style> element to the page
    document.head.appendChild(style);

    const sheet = style.sheet;
    sheet.insertRule(workaroundCss, 0);
  } catch (ex) {}
}

setTimeout(() => {
  workaroundJitterBug();
}, 1000);
