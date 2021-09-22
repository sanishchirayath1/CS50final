const addUrl = document.getElementById("add-url");
const input = document.getElementsByClassName("input");

function inputUrl() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
            input.value = tabs[0].url})
            
}