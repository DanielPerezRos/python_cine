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
            title: '¿Seguro que quieres borrar el producto?',
            text: "No podrás revertir los cambios",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, borralo'
        }).then((result) => {
            if (result.isConfirmed) {
                $(this).closest("div").hide();
                Swal.fire(
                'Borrado',
                'El producto ha sido borrado.',
                'success'
            )

            }
        })
    })   
});