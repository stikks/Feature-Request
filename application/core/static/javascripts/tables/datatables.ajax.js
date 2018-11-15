
(function( $ ) {

	'use strict';

	var datatableInit = function() {

		var $table = $('#datatable-ajax');
		$table.dataTable({
			bProcessing: true,
			sAjaxSource: $table.data('url'),
			aoColumns: [{
              mData: null,
              bSortable: false,
              mRender: function(data, type, full) {
                console.log(data, full);
                return '<a class="btn btn-info btn-sm" href=/clients/' + full[1] + '/feature-requests>' + 'Feature Requests' + '</a>';
              }
            }]
		});

	};

	$(function() {
		datatableInit();
	});

}).apply( this, [ jQuery ]);