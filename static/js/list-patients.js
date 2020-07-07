Vue.use(Vuetable);
new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    components: {
        'vuetable-pagination': Vuetable.VuetablePagination
    },
    data: {
        urlApiPatients: urlApiPatients,
        patient: {},
        addressUser: '',
        fields: [
            {
                name: 'death_rate_covid19',
                title: 'Nivel de riesgo',
                titleClass: 'center aligned',
                dataClass: 'center aligned',
                callback: 'formatRiskLevel'
            },
            {
                name: 'document',
                title: 'Número documento',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            }, 
            {
                name: 'full_name',
                title: 'Nombre',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'age',
                title: 'Edad',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'gender',
                title: 'Sexo',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'address',
                title: 'Dirección',
                titleClass: 'center aligned',
                dataClass: 'center aligned'                
            },
            {
                name: 'distance',
                title: 'Distancia',
                titleClass: 'center aligned',
                dataClass: 'center aligned',
                callback: 'setLoadingIcon'
            },
            {
                name: 'duration',
                title: 'Duración',
                titleClass: 'center aligned',
                dataClass: 'center aligned',
                callback: 'setLoadingIcon'
            },
            {
                name: 'photo',
                visible: false
            },
            {
                name: 'phone_number',
                visible: false
            },
            {
                name: 'risk_factors_display',
                visible: false
            },
            {
                name: 'symptons',
                visible: false
            },
            {
                name: 'had_contact_covid',
                visible: false
            },
            '__slot:actions'
        ],
        googleMapsAPIURL: "https://maps.googleapis.com/maps/api/distancematrix/json",
        googleMapsAPIKey: "AIzaSyDmLLWgwh9Jd_dV3JdybN868up0RXNvBRU",
    },
    methods: {
        formatRiskLevel(value){
            value = parseFloat(value);
            if(value < 50.00){
                return '<button class="ui circular low-risk icon button"><i class="icon"></i></button></button>'
            }else if(value >= 50.00 && value < 80){
                return '<button class="ui circular middle-risk icon button"><i class="icon"></i></button></button>'
            }else if(value >= 80.00){
                return '<button class="ui circular high-risk icon button"><i class="icon"></i></button></button>'
            }
        },
        setLoadingIcon(value){
            if(value){
                return value
            }
            return '<div class="ui active inline loader"></div>'
        },
        onPaginationData(paginationData) {
            this.$refs.pagination.setPaginationData(paginationData)
            navigator.geolocation.getCurrentPosition(this.loadMatrixGoogle);
        },
        onChangePage(page) {
            this.$refs.vuetable.changePage(page)
        },
        generateRoute(patient) {
            this.patient = patient
            if(patient.photo){
                this.patient['photo'] = `data:img/png;base64,${patient.photo}`;
            }else{
                this.patient['photo'] = "https://eshendetesia.com/images/user-profile.png"
            }
            //let input = document.getElementById("search-address-input");
            //google.maps.event.trigger(input, "focus", {});
            //google.maps.event.trigger(input, "keydown", {keyCode: 13});
            death_rate_covid19 = parseFloat(patient.death_rate_covid19)
            if(death_rate_covid19 < 1){
                $("#level-risk").find('.bar').width('10%');
            }else{
                $("#level-risk").find('.bar').width(`${death_rate_covid19}%`);
            }
            if(death_rate_covid19 < 50.00){
                $("#level-risk .bar").removeClass('high-risk middle-risk');
                $("#level-risk .bar").addClass('low-risk');
            }else if(death_rate_covid19 >= 50.00 && death_rate_covid19 < 80.00){
                $("#level-risk .bar").removeClass('high-risk low-risk');
                $("#level-risk .bar").addClass('middle-risk');
            }else{
                $("#level-risk .bar").removeClass('low-risk middle-risk');
                $("#level-risk .bar").addClass('high-risk');
            }
            let directionRequest = {
                origin: 'Av. brasil 2045 Lima Peru',
                destination: this.patient.address,
                provideRouteAlternatives: false,
                travelMode: 'DRIVING',
                drivingOptions: {
                    departureTime: new Date(/* now, or future date */),
                    trafficModel: 'pessimistic'
                },
                unitSystem: google.maps.UnitSystem.IMPERIAL
            }
            directionsService.route(directionRequest, function (result, status) {
                if (status == 'OK') {
                    directionsRenderer.setDirections(result);
                    $('.ui.modal').modal('show');
                }
            });
        },
        loadMatrixGoogle(position){
            data = this.$refs.vuetable["tableData"];
            self = this;
            currentLat = position.coords.latitude;
            currentLng = position.coords.longitude;
            console.log(currentLat, currentLng)
            this.showCurrentPosition
            data.map(function(person, index){
                //let addresOrigin = "Av. brasil 2045 Lima Peru";
                let addresOrigin = new google.maps.LatLng(currentLat, currentLng);
                let addrsDestination = person.address;
                var service = new google.maps.DistanceMatrixService();
                service.getDistanceMatrix(
                    {
                        origins: [addresOrigin],
                        destinations: [addrsDestination],
                        travelMode: 'DRIVING'
                    }, function (response, status) {
                        elements = response.rows[0].elements
                        if (elements) {
                            self.$refs.vuetable["tableData"][index]['distance'] = self.patient['distance'] = elements[0].distance.text
                            self.$refs.vuetable["tableData"][index]['duration'] = self.patient['duration'] = elements[0].duration.text
                        }
                    })
            })
        },
        setParamsApiPatient(params){
            let listParams = []
            Object.keys(params).map(function(key){
                listParams.push(`${key}=${params[key]}`)
            });
            this.urlApiPatients = `${this.urlApiPatients.split('?')[0]}?${listParams.join('&')}`
        },
        deleteRow(rowData) {
            alert("You clicked delete on" + JSON.stringify(rowData))
        }
    }
});