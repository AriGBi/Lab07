import database
from database.meteo_dao import MeteoDao
from model.citta import Citta


class Model:
    def __init__(self):
        self.dao=MeteoDao()
        self.costo=0
        self.M=[]
        self.T=[]
        self.G=[]
        self.Milano=Citta("Milano",0,0,self.M)
        self.Torino=Citta("Torino",0,0,self.T)
        self.Genova=Citta("Genova",0,0,self.G)
        self.percorsoMinimo=[]
        self.cittaCorrente=None

    def get_all_situazioni(self,mese):
        listaTotale=self.dao.get_all_situazioni()
        listaGenova=[]
        listaMilano=[]
        listaTorino=[]
        for s in listaTotale:
            if s.localita=="Milano" and s.creaMese()==mese:
                listaMilano.append(s.umidita)
            elif s.localita=="Torino" and s.creaMese()==mese:
                listaTorino.append(s.umidita)
            elif s.localita=="Genova" and s.creaMese()==mese:
                listaGenova.append(s.umidita)
        mediaMilano=sum(listaMilano)/len(listaMilano)
        mediaTorino=sum(listaTorino)/len(listaTorino)
        mediaGenova=sum(listaGenova)/len(listaGenova)
        return mediaMilano,mediaTorino,mediaGenova

    def get_all_situazioni_ricorsione(self,mese):
        lista=self.dao.get_all_situazioni_ricorsione(mese)
        for s in lista:
            if s.localita=="Milano":
                self.M.append(s)
            elif s.localita=="Torino":
                self.T.append(s)
            else:
                self.G.append(s)

    def recursion(self,giorno):

        if giorno==15:
            #stampa il self.costo
            #stampa la situazione con il toString per s in percorso minimo
            pass
        if giorno==0:
            m=min(self.M[0].umidita,self.T[0].umidita,self.G[0].umidita)
            if m==self.Milano.listaSituazioni[0].umidita:
                self.cittaCorrente=self.Milano

            elif m==self.T[0].umidita:
                self.cittaCorrente=self.Torino
            elif m==self.G[0].umidita:
                self.cittaCorrente=self.Genova


            self.cittaCorrente.giorniTot += 1
            self.cittaCorrente.giorniCons += 1
            self.percorsoMinimo.append(self.M[0])
            self.recursion(giorno + 1)
