import pytest
import Func_Plotter


@pytest.fixture
def app(qtbot):
    test_app = Func_Plotter.MainWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture(scope='function', autouse=True)
def req_app(app, request):
    request.instance.app = app

#class for testing normal case
class Test_general:

    # test that error_dialog is hidden in normal case
    def test_no_error_dialog(self, request):
        assert request.instance.app.error_dialog.isHidden() == True

    # test submit button text
    def test_submit_text(self, request):
        assert request.instance.app.submit.text() == "Plot"

# Class for testing function
class Test_funcion:
    # test that function is an enabled text box
    def test_enabled(self, request):
        assert request.instance.app.function.isEnabled() == True

    # test writing on test box
    def test_editable(self, request):
        assert request.instance.app.function.isReadOnly() == False

    # test that on_change signal is running when click 'plot'
    def test_onchange_signal(self, request, qtbot):
        with qtbot.waitSignal(request.instance.app.submit.clicked, timeout=10000):
            request.instance.app.submit.click()

#class for testing different cases of expression
class Test_validation:
    # error_dialog isn't shown if valid expression is written
    def test_function_valid1(self, request):
        request.instance.app.function.setText("x+5")
        request.instance.app.submit.click()
        assert request.instance.app.error_dialog.isHidden() == True

    def test_function_valid2(self, request):
        request.instance.app.function.setText("x^2+x")
        request.instance.app.submit.click()
        assert request.instance.app.error_dialog.isHidden() == True

    # error_dialog is shown if not valid expression is written
    def test_function_error1(self, request):
        request.instance.app.function.setText("5y+x")
        request.instance.app.submit.click()
        assert request.instance.app.error_dialog.isHidden() == False

    def test_function_error2(self, request):
        request.instance.app.function.setText("yx")
        request.instance.app.submit.click()
        assert request.instance.app.error_dialog.isHidden() == False


#test min max values
class Test_spinbox:

    # test that box of min x is editable
    def test_mn_editable(self, request):
        assert request.instance.app.mn.isReadOnly() == False

    # test that box of min x is enabled
    def test_mn_enabled(self, request):
        assert request.instance.app.mn.isEnabled() == True

    # test that box of max x is editable
    def test_mx_editable(self, request):
        assert request.instance.app.mx.isReadOnly() == False

    # test that box of max x is enabled
    def test_mx_enabled(self, request):
        assert request.instance.app.mx.isEnabled() == True

    # test min x initial value
    def test_mn_initial(self, request):
        assert request.instance.app.mn.value() == -10

    # test max x starting value
    def test_x_initial(self, request):
        assert request.instance.app.mx.value() == 10

    # test minimum range of x
    def test_minimum_value(self, request):
        assert request.instance.app.mn.minimum() == -100

    # test maximum range of x
    def test_maximum_value(self, request):
        assert request.instance.app.mn.maximum() == 100

    # test that increasing value is allowed
    def test_increase_max(self, request):
        request.instance.app.mx.stepBy(2)
        assert request.instance.app.mx.value() == 12

    def test_increase_min(self, request):
        request.instance.app.mn.stepBy(5)
        assert request.instance.app.mn.value() == -5


    # test that decreasing value is allowed
    def test_increase_max(self, request):
        request.instance.app.mx.stepBy(-5)
        assert request.instance.app.mx.value() == 5

    def test_increase_min(self, request):
        request.instance.app.mn.stepBy(-10)
        assert request.instance.app.mn.value() == -20

    # error_dialog is shown if max x is smaller then min x
    def test_min_max(self, request):
        request.instance.app.mn.setValue(5)
        request.instance.app.mx.setValue(3)
        assert request.instance.app.error_dialog.isHidden() == False