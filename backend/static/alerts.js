function createAlert(msg, tag) {
    var html = `<div class="alert ${
        tag == "success" ? "alert-success" : "alert-danger"
    } message-animation" >${msg}</div>`;
    return html;
}

htmx.on("messages", function (e) {
    var messageContainer = document.querySelector("[data-message-container]");
    var messages = e.detail.value;

    messages.forEach((msg) => {
        var alert = createAlert(msg.message, msg.tags);
        messageContainer.insertAdjacentHTML("beforeEnd", alert);
    });
});
