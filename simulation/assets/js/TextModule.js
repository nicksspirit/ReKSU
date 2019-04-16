var TextModule = function() {
    let tag = "<div class='lead'></div>";
    let text = $(tag)[0];

    // Append text tag to #sidebar:
    $("#sidebar").append(text);

    this.render = function(data) {
        $(text).html(data);
    };

    this.reset = function() {
        $(text).html("");
    };
};