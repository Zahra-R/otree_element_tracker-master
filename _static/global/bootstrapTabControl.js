function bootstrapTabControl(){
    var i, items = $('.nav-link'), pane = $('.tab-pane');
    // Next
    $('.nexttab').on('click', function(){
        for(i = 0; i < items.length; i++){
            if($(items[i]).hasClass('active') == true){
                break;
            }
        }
        if(i < items.length - 1){
            // for tab
            $(items[i]).removeClass('active');
            $(items[i+1]).addClass('active');
            // for pane
            $(pane[i]).removeClass('show active');
            $(pane[i+1]).addClass('show active');
        }
    });
    // Prev
    $('.prevtab').on('click', function(){
        for(i = 0; i < items.length; i++){
            if($(items[i]).hasClass('active') == true){
                break;
            }
        }
        if(i != 0){
            // for tab
            $(items[i]).removeClass('active');
            $(items[i-1]).addClass('active');
            // for pane
            $(pane[i]).removeClass('show active');
            $(pane[i-1]).addClass('show active');
        }
    });
  }
  $(document).ready(function(){
      bootstrapTabControl();
  });
  