let actual = 0;
let previous = 0;

$(".next").click(function(){
  if (actual == 0) {
    actual++;
    $('.stage' + actual).show();
    $('.stage' + previous).hide();
    $('.bar' + actual).addClass('active');
  } else {  
    previous = actual;
    actual++;
    $('.stage' + actual).show();
    $('.stage' + previous).hide();
    $('.bar' + actual).addClass('active');
  }
});

$(".previous").click(function(){
  if (previous == 0) {
    actual = previous;
    $('.stage' + actual).show();
    $('.stage' + (actual + 1)).hide();
    $('.bar' + (actual + 1)).removeClass('active');
  } else {
    actual = previous;
    previous--;
    $('.stage' + actual).show();
    $('.stage' + (actual + 1)).hide();
    $('.bar' + (actual + 1)).removeClass('active');
  }
});
jQuery('#edeviceSelect').multiselect({
    columns: 3,
    placeholder: 'Select Devices...',
    search: true,
    selectAll: true 
});

jQuery('#mobiledeviceSelect').multiselect({
    columns: 2,
    placeholder: 'Select Devices...',
    search: true,
    selectAll: true
});

jQuery('#sensordeviceSelect').multiselect({
  columns: 3,
  placeholder: 'Select Languages',
  search: true,
  selectAll: true
});

jQuery('#sensordataSelect').multiselect({
  columns: 2,
  placeholder: 'Select Languages',
  search: true,
  selectAll: true
});

jQuery('#accdataSelect').multiselect({
  columns: 2,
  placeholder: 'Select Languages',
  search: true,
  selectAll: true
});

