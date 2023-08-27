if (!window.dash_clientside) {
    window.dash_clientside = {};
    var __rendezvouz_setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;

}
window.dash_clientside.clientside = {
    make_draggable_mre: function (id) {
        setTimeout(function () {
            var el = document.getElementById(id)
            window.console.log(el)
            dragul = dragula([el])
            dragul.on("drop", function (el, target, source, sibling) {
                var result = {
                    'element': el.id,
                    'target_id': target.id,
                    'target_children': Array.from(target.children).map(function (child) {return child.id;})
                    }              
                if (source.id != target.id) {
                    result['source_id'] = source.id;
                    result['source_children'] = Array.from(source.children).map(function (child) {return child.id;});
				}
                var client_event_receiver = document.getElementById("client_event_receiver");
                __rendezvouz_setter.call(client_event_receiver, JSON.stringify(result));
                var client_event = new Event('input', { bubbles: true });
                client_event_receiver.dispatchEvent(client_event);
                    
            })
        }, 1)
        return window.dash_clientside.no_update
    }
}