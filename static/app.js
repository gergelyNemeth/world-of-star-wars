$(document).ready(function(){
    $('.residents').on('click', function(event){
        var planetName = event.target.dataset.planet;
        var planetUrl = event.target.dataset.url.replace('http://', 'https://');
        $('#planetResidents').on('show.bs.modal', function(event){
            $('.modal-title').text('Residents of ' + planetName);
        })
        
        /* remove content if exists*/
        $('.modal-body').children().remove();

        $('<div>', {
            class: 'container',
            id: 'loading',
            html: 'Loading...'
        }).appendTo('.modal-body')

        $.getJSON(planetUrl, function(data){
            var modalTableHeader = 
                `<thead>
                    <tr>
                        <th>Name</th>
                        <th>Height</th>
                        <th>Mass</th>
                        <th>Hair color</th>
                        <th>Skin color</th>
                        <th>Eyes color</th>
                        <th>Birth year</th>
                        <th>Gender</th>
                    </tr>
                </thead>`;
            var residentsTable = modalTableHeader + '<tbody id="modal-content"></tbody>'

            var keyList = ['name', 'height', 'mass', 'skin_color', 'hair_color', 'eye_color', 'birth_year', 'gender'] 
            var items = '';

            $('#loading').remove();
            $('<table>', {
                'class': 'table table-bordered',
                'id': 'residents-table',
                html:  residentsTable
            }).appendTo('.modal-body');

            $.each(data.residents, function(key, value) {
                value = value.replace('http://', 'https://');
                $.getJSON(value, function(data){
                    $.each(data, function(key, value){
                        if ($.inArray(key, keyList) > -1) {
                            if (key === 'height') {
                                value = parseFloat(Number(value) / 100) + ' m';
                            }
                            if (key === 'mass' && value !== 'unknown') {
                                value += ' kg'
                            }
                            items += ('<td>' + value + '</td>');
                        }
                    })
                    $('<tr>', {
                        html: items
                    }).appendTo('#modal-content')
                    items = '';
                })
            });
        })
        .fail(function() {
            $('#loading').remove();
            $('<div>', {
                class: 'container',
                id: 'connection-error',
                html: '<p>Cannot connect to Star Wars API.</p><p>Please try it later.</p>'
            }).appendTo('.modal-body')
        });
    })
})