 $(document).ready(function() {
            const getCookieValue = (name) => (document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || '')

            if (!getCookieValue("gridX")) {
                $("#gridX").val(41)
            } else {
               $("#gridX").val(getCookieValue("gridX") )
            }

            if (!getCookieValue("gridY")) {
                $("#gridY").val(41)
            } else {
               $("#gridY").val(getCookieValue("gridY") )
            }

            if (!getCookieValue("algorithm")) {
                $("#algorithm").val("1")
            } else {
               $("#algorithm").val(getCookieValue("algorithm") )
            }

            $('#changeGridSubmit').click(function (){
                document.cookie = "gridX=" + $("#gridX").val()
                document.cookie = "gridY=" + $("#gridY").val()
                location.reload(true)
            });

            let isMouseDown = false;
            let wall = false;
            let start = false;
            let end = false;
            $('.grid-item').mousedown(function() {
                isMouseDown = true;
                if (wall) {
                    $(this).removeClass("start").removeClass("visited").removeClass("end")
                    $(this).toggleClass("wall");
                } else if (start) {
                    $('.grid-item').removeClass("start")
                    $(this).removeClass("wall").removeClass("visited").removeClass("end");
                    $(this).toggleClass("start");
                } else if (end) {
                    $('.grid-item').removeClass("end")
                    $(this).removeClass("wall").removeClass("start").removeClass("visited")
                    $(this).toggleClass("end");
                }
            })
            .mouseup(function() {
                isMouseDown = false;
            }).mouseenter(function() {
                if(isMouseDown && wall){
                    $(this).toggleClass("wall");
                }
            });

            $('#start').click(function (){
                const start = $('.start').get(0).id.slice(1);
                const end = $('.end').get(0).id.slice(1);
                const walls = [];
                $('.wall').each(function() {
                    walls.push(this.id.slice(1));
                });

                walls.toString()
                document.cookie = "start=" + start + ";"
                document.cookie = "end=" + end + ";"
                document.cookie = "walls=" + walls + ";"
                document.cookie = "algorithm=" + $("#algorithm").val() + ";"

                const source = new EventSource('/');
                source.onmessage = function(e) {
                    if (e.data.startsWith("x")){
                        $('#' + e.data.slice(1)).addClass("path");
                    } else if (e.data.startsWith("i")) {
                        $('#' + e.data).addClass("visited");
                    }else {
                        source.close()
                    }

                }
            });

            $('#reset').click(function (){
                $('.grid-item').removeClass("wall").removeClass("start").removeClass("visited").removeClass("end").removeClass("path");
            });

            $('#start_marker').click(function (){
                $('.marker_buttons').prop('disabled', false);
                $(this).prop('disabled', true);
                start = true;
                wall = false;
                end = false;
            });

            $('#wall_marker').click(function (){
                $('.marker_buttons').prop('disabled', false)
                $(this).prop('disabled', true)
                start = false;
                wall = true;
                end = false;

            });

            $('#end_marker').click(function (){
                $('.marker_buttons').prop('disabled', false)
                $(this).prop('disabled', true)
                start = false;
                wall = false;
                end = true;
            });

        });