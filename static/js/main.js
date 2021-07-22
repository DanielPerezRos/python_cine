/* Borrado normal
$(function () {
    $(".boton-borrar").click(function() {
        if(confirm("¿Seguro que quieres borrar el producto?")){
            $(this).closest("tr").hide();
        }
    })
});
*/

// Borrado con sweetalert2
$(function () {
    $(".boton-borrar").click(function() {
        Swal.fire({
            title: '¿Seguro que quieres borrar?',
            text: "No podrás revertir los cambios",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, borra'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = 'http://127.0.0.1:8000' + $(this).attr('custom-href');
                //$(this).closest("div").hide();
                Swal.fire(
                'Borrado',
                'El borrado se ha efectuado.',
                'success'
            )

            }
        })
    })

    $('#id_image').change(function(e) {
      addImage(e);
     });

     function addImage(e){
      var file = e.target.files[0],
      imageType = /image.*/;

      if (!file.type.match(imageType))
       return;

      var reader = new FileReader();
      reader.onload = fileOnload;
      reader.readAsDataURL(file);
     }

     function fileOnload(e) {
      var result=e.target.result;
      $('#imgSalida').attr("src",result);
     }

     $('#id_national_flag').change(function(e) {
      addImage(e);
     });

     function addImage(e){
      var file = e.target.files[0],
      imageType = /image.*/;

      if (!file.type.match(imageType))
       return;

      var reader = new FileReader();
      reader.onload = fileOnload;
      reader.readAsDataURL(file);
     }

     function fileOnload(e) {
      var result=e.target.result;
      $('#imgSalida').attr("src",result);
     }

     $('#id_logo').change(function(e) {
      addImage(e);
     });

     function addImage(e){
      var file = e.target.files[0],
      imageType = /image.*/;

      if (!file.type.match(imageType))
       return;

      var reader = new FileReader();
      reader.onload = fileOnload;
      reader.readAsDataURL(file);
     }

     function fileOnload(e) {
      var result=e.target.result;
      $('#imgSalida').attr("src",result);
     }


});