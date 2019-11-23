// import deepAssign from "deep-assign";
import { serverPath } from "utils/serverPath";

export function getAppRoot(defaultRoot = "/") {
    // try configs
    let root = defaultRoot;
    console.debug(root + "Debug 1");
    try {
        root = window.galaxyConfig.options.root;
        console.debug(root + "Debug 2");
    } catch (err) {
        // console.warn("galaxyConfig not defined");
        try {
            root = getRootFromIndexLink(defaultRoot);
            console.debug(root + "Debug 3");
        } catch (err) {
            console.warn("Unable to find index link in head", err);
        }
    }
    console.debug(root + "Debug 4");
    return root;
}

// finds <link> in head element and pulls root url fragment from there
function getRootFromIndexLink(defaultRoot = "/") {
    let links = document.getElementsByTagName("link");
    let indexLink = [...links].find(link => link.rel == "index");
    if (indexLink && indexLink.href) {
        console.debug(serverPath(indexLink.href) + "Debug 5");
        return serverPath(indexLink.href);
    }
    console.debug(defaultRoot + "Debug 6");
    return defaultRoot;
}
