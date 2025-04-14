import copy

import database
from database.meteo_dao import MeteoDao
from model.citta import Citta


class Model:
    def __init__(self):
        self.dao=MeteoDao()
        self.n_soluzione=0
        self.costo_ottimo = -1
        self.soluzione_ottima = []




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

    #per la ricorsione --> prima trovo una sequenza di tutte le possibili città
    #successivamente applico i vincoli
    #infine, tra tutte le soluzioni che ho trovato, tengo solo quella con costo minore

    def calcola_sequenza(self,mese):
        self.costo_ottimo=-1
        self.soluzione_ottima=[]
        situazioni = MeteoDao.get_all_situazioni_meta_mese(mese)
        self._recursion([],situazioni)
        return self.soluzione_ottima, self.costo_ottimo


    def _recursion(self,parziale,lista_situazioni):
        #condizione terminale:
        if len(parziale)==15:
            self.n_soluzione+=1
            costo=self._calcola_costo(parziale)
            if self.costo_ottimo==-1 or self.costo_ottimo>costo:
                self.costo_ottimo=costo
                self.soluzione_ottima= copy.deepcopy(parziale)
            #print(f"costo = {costo} |||| {parziale}")

        #condizione ricorsiva:
        else:
            #cercare le città per il giorno che mi serve
            candidates=self.trova_possibili_step(parziale,lista_situazioni) #funzione che sulla base di quanti elementi ho dentro a parziale, va a prendere dentro la lista di tutte le  situazioni quelle relative al giorno che mi serve
            #provo ad aggiungere una di queste citta e vado avanti
            for candidate in candidates:
                # dati i possibili candidati, devo verificare i vincoli --> se i vincoli sono soddisfatti faccio l'append
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._recursion(parziale,lista_situazioni)
                    parziale.pop()

    def trova_possibili_step(self,parziale,lista_situazioni):
        giorno = len(parziale)+1 #se il mio parziale ha il giorno 1, a me serve cercare il giorno 2
        candidati=[]
        for situazione in lista_situazioni:
            if situazione.data.day==giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self,candidate, parziale):
        """ dato un candidato devo vedere se soddisfa i vincoli, rispetto a quali città ho nella lista parziale"""
        #primo vincolo --> una città non può comparire nella sequenza piu di 6 volte
        counter=0
        for situazione in parziale:
            if situazione.localita==candidate.localita:
                counter+=1
        if counter>=6:
            return False
        #secondo vincolo --> bisonga rimanere nella città almeno 3 giorni
        #per sapere se posso mettere la Città in un punto, devo vedere cosa succede i 3 giorni precedenti
        #se i 3 giorni precedenti sono uguali, ho già rispettato il vincolo di permanenza e allora posso mettere la città che voglio
        #se invece i 3 giorni precedenti non sono uguali, allora devo sicuramente mettere la città che c'è in precedenza
        # se però sono all'inizio della lista, quindi in seconda posizione --> non posos guardare i 3 giorni precedenti perchè non ci sono. So per certo però che se il vettore è piu piccolo di 3, la seconda città deve essere uguale alla prima e anche la terza

        #caso1) lunghezza di parziale minore di 3
        if len(parziale)==0: #se non ho ancora nessuna città, qualsiasi candidato va bene
            return True
        if len(parziale)<3 :
            if candidate.localita != parziale[0].localita:
                return False

        #caso2) le 3 situaizoni precedenti non sono tutte uguali
        else:
            if parziale[-3].localita != parziale[-2].localita or parziale[-1].localita != parziale[-2].localita or parziale[-3].localita != parziale[len(parziale)-1].localita:
                if parziale[-1].localita != candidate.localita:
                    return False

        #se supera i vincoli:
        return True

    def _calcola_costo(self,parziale):
        costo=0
        for i in range(len(parziale)):
            costo+=parziale[i].umidita #costo fisso per ogni citta

        for i in range(len(parziale)):
            #se i 2 giorni precedenti non sono stato nella stessa città in cui sono ora, pago 100
            if i>=2 and (parziale[i].localita!=parziale[i-1].localita or parziale[i].localita!=parziale[i-2].localita): #c'è i>2 perchè tanto  i primi due giorni sarò sicuramente nella stessa città
                costo+=100
        return costo


if __name__ == '__main__':
    my_model=Model()
    print(my_model.calcola_sequenza(2))
    print(my_model.n_soluzione)

