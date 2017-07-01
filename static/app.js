$(document).ready(function(){
    $('.residents').on('click', function(event){
        var planetName = event.target.dataset.planet;
        var planetUrl = event.target.dataset.url.replace('http://', 'https://');
        $('#planetResidents').on('show.bs.modal', function(event){
            $('.modal-title').text('Residents of ' + planetName);
        })
        
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
        /* remove content if exists*/
        $('.modal-body').children().detach();
        $('<table>', {
            'class': 'table table-bordered',
            'id': 'residentsTable',
            html:  residentsTable
        }).appendTo('.modal-body');

        $.getJSON(planetUrl, function(data){
            var keyList = ['name', 'height', 'mass', 'skin_color', 'hair_color', 'eye_color', 'birth_year', 'gender'] 
            var items = '';

            $('<div>', {
                class: 'container',
                id: 'loading',
                html: 'Loading...'
            }).appendTo('.modal-body')

            $.each(data.residents, function(key, value) {
                value = value.replace('http://', 'https://');
                $.getJSON(value, function(data){
                    $('#loading').remove()
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
        });
    })
})