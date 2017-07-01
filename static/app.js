$(document).ready(function(){
    $('.residents').on('click', function(e){
        var planetName = e.target.dataset.planet;
        var planetUrl = e.target.dataset.url.replace('http://', 'https://');
        $('#planetResidents').on('show.bs.modal', function(e){
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
        $('.modal-body').children().detach(); /* remove content if exists*/
        $('<table>', {
            'class': 'table table-bordered',
            'id': 'residentsTable',
            html:  residentsTable
        }).appendTo('.modal-body');

        $.getJSON(planetUrl, function(data){
            var keyList = ['name', 'height', 'mass', 'skin_color', 'hair_color', 'eye_color', 'birth_year', 'gender'] 
            var items = '';
            $.each(data.residents, function(key, val) {
                val = val.replace('http://', 'https://');
                $.getJSON(val, function(data){
                    $.each(data, function(key, val){
                        if ($.inArray(key, keyList) > -1) {
                            if (key === 'height') {
                                val = parseFloat(Number(val) / 100) + ' m';
                            }
                            if (key === 'mass' && val !== 'unknown') {
                                val += ' kg'
                            }
                            items += ('<td>' + val + '</td>');
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