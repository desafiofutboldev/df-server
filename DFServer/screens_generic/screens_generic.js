$(document).ready(function () {

    console.log("Screens ready");

    // Ocultar todas y mostrar idle por defecto
    $(".screen").hide();
    $("#idle").show();

    // Insertar valores del servidor
    $(".gameName").html(`{{ gameName }}`);
    $(".gameUnit").html(`{{ gameUnit }}`);
    $(".playingTitle").html(`{{ playingTitle }}`);

    // Ajustar tamaño del título grande
    function adjustFontSize() {
        const $gameName = $(".gameName");
        const $parent = $gameName.parent();
        const parentWidth = $parent.width();

        $gameName.css("font-size", "130px");

        let fontSize = 130;
        let updated = false;

        while ($gameName[0].scrollWidth > parentWidth && fontSize > 10) {
            updated = true;
            fontSize--;
            $gameName.css("font-size", fontSize + "px");
        }

        if (updated) {
            fontSize -= 3;
            $gameName.css("font-size", fontSize + "px");
        }
    }

    adjustFontSize();
});

// Socket listeners
const socket = io("http://127.0.0.1:5000");

socket.on("changeScreen", function (data) {
    console.log("changeScreen", data.screenId);
    $(".screen").hide();
    $("#" + data.screenId).show();
});

socket.on("updateParam", function (data) {
    console.log("updateParam", data.paramValue);
    $("." + data.paramClass).html(data.paramValue);
});
