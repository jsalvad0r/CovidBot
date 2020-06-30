Vue.use(Vuetable);
new Vue({
    el: '#app',
    components: {
        'vuetable-pagination': Vuetable.VuetablePagination
    },
    data: {
        userProfileImg: '',
        addressUser: '',
        fields: [
            {
                name: 'document_type',
                title: 'Tipo documento',
                titleClass: 'center aligned',
                dataClass: 'center aligned'
            },
            {
                name: 'document_number',
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
            '__slot:actions'
        ],
        googleMapsAPIURL: "https://maps.googleapis.com/maps/api/distancematrix/json",
        googleMapsAPIKey: "AIzaSyDmLLWgwh9Jd_dV3JdybN868up0RXNvBRU",
    },
    methods: {
        setLoadingIcon(value){
            if(value){
                return value
            }
            return '<div class="ui active inline loader"></div>'
        },
        onPaginationData(paginationData) {
            this.$refs.pagination.setPaginationData(paginationData)
            this.loadMatrixGoogle();
        },
        onChangePage(page) {
            this.$refs.vuetable.changePage(page)
        },
        generateRoute(photo, address) {
            this.userProfileImg = `data:img/png;base64,${photo}`;
            this.addressUser = address;
            let input = document.getElementById("search-address-input");
            //google.maps.event.trigger(input, "focus", {});
            //google.maps.event.trigger(input, "keydown", {keyCode: 13});
            let directionRequest = {
                origin: 'Av. brasil 2045 Lima Peru',
                destination: address,
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
        loadMatrixGoogle(){
            data = this.$refs.vuetable["tableData"];
            self = this;
            data.map(function(person, index){
                let addresOrigin = "Av. brasil 2045 Lima Peru";
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
                            self.$refs.vuetable["tableData"][index]['distance'] = elements[0].distance.text
                            self.$refs.vuetable["tableData"][index]['duration'] = elements[0].duration.text
                        }
                    })
            })
        },
        deleteRow(rowData) {
            alert("You clicked delete on" + JSON.stringify(rowData))
        }
    }
});