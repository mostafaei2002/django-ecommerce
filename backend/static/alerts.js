function createAlert(msg, tag) {
    var html = `<div class="toast text-bg-${tag} align-items-center border-0 show message-animation" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
            <div class="toast-body">
            ${msg}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    </div>`;
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
