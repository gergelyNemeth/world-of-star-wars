$(document).ready(function(){
    $('.residents').on('click', function(e){
        var planetName = e.target.dataset.planet;
        var planetUrl = e.target.dataset.url;
        $('#planetResidents').on('show.bs.modal', function(e){
            $('.modal-title').text('Residents of ' + planetName);
        })
    })
})