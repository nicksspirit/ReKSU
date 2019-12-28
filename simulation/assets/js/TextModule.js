var TextModule = function() {
  let tag = $("<div class='lead'></div>")

  // Append text tag to #sidebar:
  $('#sidebar').append(tag)

  this.render = function(data) {
    tag.html(data)
  }

  this.reset = function() {
    tag.html('')
  }
}
