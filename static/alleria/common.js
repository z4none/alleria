//

function createZtree() {
    var selectedNode = null

    function onClick(e, treeId, node, flag) {
        selectedNode = node;
    }

    function onMouseUp(event, treeId, treeNode) {
        if(treeNode === null) {
            tree.cancelSelectedNode();
            selectedNode = null;
        }
    }

    function loadData(url, el, id) {
        $.ajax({
            url: url,
            dataType: "json"
        }).then(function(response){
            tree = $.fn.zTree.init(el, {
                data: {
                    simpleData: {
                        enable: true,
                        idKey: "id",
                        pIdKey: "parent_id",
                        rootPId: null
                    }
                },
                callback: {
                    onClick: onClick,
                    onMouseUp: onMouseUp
                }
            }, response.items);

            tree.expandAll(true);

            if(id !== undefined) {
                var node  =tree.getNodeByParam("id", id.toString());
                tree.selectNode(node);
            }
            else {
                tree.cancelSelectedNode();
            }
        });
    }

    function getSelectedNode(){
        return selectedNode;
    }


    return {
        loadData: loadData,
        getSelectedNode: getSelectedNode
    }
}



$(function(){
    // multiple selectpicker
    $('select[multiple="multiple"]').selectpicker({});

    // ztree
    $("input[role='ztree']").click(function(){
        var displayField = $(this);
        var hiddenField = $("#" + displayField.attr("id") + "-hidden");
        var tree = createZtree();
        var dialog = $("#" + $(this).data("dialog"));
        var url = $(this).data("url");

        dialog.one("show.bs.modal", function(){
            var el = dialog.find(".ztree");
            el.html("");
        }).one("shown.bs.modal", function(){
            var el = dialog.find(".ztree");
            tree.loadData(url, el, hiddenField.val());
        });

        dialog.find(".btn-ok").one("click", function(){
            var node = tree.getSelectedNode();
            if(node) {
                displayField.val(node.name);
                hiddenField.val(node.id);
            }
            dialog.modal("hide");
        })

        dialog.modal();
    })
});