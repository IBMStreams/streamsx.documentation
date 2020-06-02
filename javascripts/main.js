
$(document).ready(function(){
  var h1h2 = $("h1, h2")
 h1h2.each(function(){
	var sidebar = $("ul.nav-sidebar");
    sidebar.append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a class='toc' href='#" + $(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,'') + "'> " + $(this).text() + "</a></li>");
    $(this).attr("id",$(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,''));
  });

  // Handle open/close accordion for FAQ page
  var accordions = $(".faq-accordion");
  if (accordions.length > 0) {
    accordions.each(function() {
      $(this).click(function() {
        $(this).toggleClass("active");
        var accordionPanel = $(this).next(".faq-accordion-panel");
        if (accordionPanel.css("maxHeight") !== "0px") {
          accordionPanel.css("maxHeight", 0);
        } else {
          accordionPanel.css("maxHeight", "none");
        }
      });
    });
  }

  // Handle expand/collapse all buttons for FAQ page
  var expandAllBtn = $(".faq-expand-all");
  var collapseAllBtn = $(".faq-collapse-all");
  if (expandAllBtn && accordions.length > 0) {
    expandAllBtn.click(function() {
      accordions.each(function() {
        $(this).addClass("active");
        $(this).next(".faq-accordion-panel").css("maxHeight", "none");
      });
    });
  }
  if (collapseAllBtn && accordions.length > 0) {
    collapseAllBtn.click(function() {
      accordions.each(function() {
        $(this).removeClass("active");
        $(this).next(".faq-accordion-panel").css("maxHeight", 0);
      });
    });
  }

  // Handle anchor link clicks in left sidebar for FAQ page
  var adjustAnchorLink = function() {
    var anchorLink = $(":target");
    var elemHeight = 75;
    if (anchorLink.length > 0) {
      $("html, body")
        .stop()
        .animate({
          scrollTop: anchorLink.offset().top - elemHeight
        }, 200);
    }
  };
  $(window).on("hashchange load", function() {
    if (window.location.pathname.includes("/streamsx.documentation/docs/spl/quick-start/qs-3")) {
      adjustAnchorLink();
    }
  });
});
