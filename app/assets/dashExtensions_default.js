window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        point_to_layer: function(feature, latlng, context){
            const {circleOptions} = context.hideout;
            return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
        }
    }
});