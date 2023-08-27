window.dash_props = Object.assign({}, window.dash_props, {
    module: {
        on_each_feature: function (feature, layer, context) {
            if (!feature.properties) {
                return
            }
            if (feature.properties) {
                layer.bindPopup(feature.properties)
            }
        }
    }
});