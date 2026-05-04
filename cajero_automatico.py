import wx

# --- LÓGICA DEL CAJERO (Clase de Negocio) ---
class CajeroCorriente:
    def __init__(self, saldo_inicial=1000):
        self.__saldo = saldo_inicial  # Atributo privado

    def consultar_saldo(self):
        return self.__saldo

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            return True, f"Depósito exitoso. Nuevo saldo: ${self.__saldo}"
        return False, "El monto debe ser mayor a cero."

    def retirar(self, monto):
        if monto <= 0:
            return False, "Monto inválido."
        if monto <= self.__saldo:
            self.__saldo -= monto
            return True, f"Retiro exitoso. Saldo restante: ${self.__saldo}"
        return False, "Fondos insuficientes."

# --- INTERFAZ GRÁFICA ---
class VentanaCajero(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simulador de Cajero Automático', size=(350, 400))
        self.cajero = CajeroCorriente()
        self.configurar_interfaz()
        self.Show()

    def configurar_interfaz(self):
        panel = wx.Panel(self)
        contenedor = wx.BoxSizer(wx.VERTICAL)

        # Estética y fuentes
        fuente_saldo = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.label_bienvenida = wx.StaticText(panel, label="Bienvenido a su Banca Digital")
        self.label_saldo = wx.StaticText(panel, label=f"Saldo Disponible: ${self.cajero.consultar_saldo()}")
        self.label_saldo.SetFont(fuente_saldo)

        self.entrada_monto = wx.TextCtrl(panel, placeholderText="Ingrese monto aquí...")
        
        # Botones
        self.btn_depositar = wx.Button(panel, label="Depositar")
        self.btn_retirar = wx.Button(panel, label="Retirar")
        self.btn_salir = wx.Button(panel, label="Finalizar")

        # Eventos
        self.btn_depositar.Bind(wx.EVT_BUTTON, self.al_depositar)
        self.btn_retirar.Bind(wx.EVT_BUTTON, self.al_retirar)
        self.btn_salir.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        # Layout
        elementos = [self.label_bienvenida, self.label_saldo, self.entrada_monto, 
                     self.btn_depositar, self.btn_retirar, self.btn_salir]
        
        for el in elementos:
            contenedor.Add(el, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(contenedor)

    def actualizar_pantalla(self):
        self.label_saldo.SetLabel(f"Saldo Disponible: ${self.cajero.consultar_saldo()}")
        self.entrada_monto.Clear()

    def mostrar_mensaje(self, mensaje, titulo="Aviso"):
        dlg = wx.MessageDialog(self, mensaje, titulo, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def al_depositar(self, event):
        try:
            monto = float(self.entrada_monto.GetValue())
            exito, msj = self.cajero.depositar(monto)
            self.mostrar_mensaje(msj)
            if exito: self.actualizar_pantalla()
        except ValueError:
            self.mostrar_mensaje("Por favor, ingrese un número válido.", "Error")

    def al_retirar(self, event):
        try:
            monto = float(self.entrada_monto.GetValue())
            exito, msj = self.cajero.retirar(monto)
            self.mostrar_mensaje(msj)
            if exito: self.actualizar_pantalla()
        except ValueError:
            self.mostrar_mensaje("Por favor, ingrese un número válido.", "Error")

if __name__ == '__main__':
    app = wx.App()
    VentanaCajero()
    app.MainLoop()
