document.getElementById('nuovaEmissione').addEventListener('click', function() {
    document.getElementById('tipoEmissione').classList.add('active');
    document.getElementById('sfondo').style.filter = 'blur(3px)';
  });

document.getElementById('tipoEmissione').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('active');
        document.getElementById('sfondo').style.filter = 'none';
    }
});

document.getElementById('trasporti').addEventListener('click', function() {
    document.getElementById('tipoTrasporti').classList.add('active');
    document.getElementById('tipoEmissione').classList.remove('active');
});

document.getElementById('tipoTrasporti').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('active');
        document.getElementById('sfondo').style.filter = 'none';
    }
});

document.getElementById('confermaEmissione').addEventListener('click', function() {
    document.getElementById('tipoTrasporti').classList.remove('active');
    document.getElementById('sfondo').style.filter = 'none';
});


document.getElementById('energia').addEventListener('click', function() {
    document.getElementById('tipoEnergia').classList.add('active');
    document.getElementById('tipoEmissione').classList.remove('active');
});

document.getElementById('tipoEnergia').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('active');
        document.getElementById('sfondo').style.filter = 'none';
    }
});

document.getElementById('confermaEnergia').addEventListener('click', function() {
    document.getElementById('tipoEnergia').classList.remove('active');
    document.getElementById('sfondo').style.filter = 'none';
});


document.getElementById('cibo').addEventListener('click', function() {
    document.getElementById('tipoCibo').classList.add('active');
    document.getElementById('tipoEmissione').classList.remove('active');
});

document.getElementById('tipoCibo').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('active');
        document.getElementById('sfondo').style.filter = 'none';
    }
});

document.getElementById('confermaCibo').addEventListener('click', function() {
    document.getElementById('tipoCibo').classList.remove('active');
    document.getElementById('sfondo').style.filter = 'none';
});

