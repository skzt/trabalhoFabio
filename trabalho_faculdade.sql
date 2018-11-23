drop database faculdade;
create database faculdade;
use faculdade;

CREATE TABLE `ALUNO` (
  `idAluno` INT(10) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  `cpf` INT(11) NULL,
  `dataNascimento` VARCHAR(45) NULL,
  `curso` VARCHAR(45) NULL,
  PRIMARY KEY (`idAluno`))
ENGINE = InnoDB;

CREATE TABLE `LOGIN` (
  `idUsuario` INT(10) NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  `idAluno` INT(10) NOT NULL UNIQUE,
  PRIMARY KEY (`idUsuario`),
  CONSTRAINT FK_idAluno1 FOREIGN KEY(idAluno) REFERENCES ALUNO(idAluno)
  ON DELETE CASCADE
  ON UPDATE CASCADE
)ENGINE = InnoDB;

CREATE TABLE `DISCIPLINA` (
  `idDisciplina` INT(10) NOT NULL AUTO_INCREMENT,
  `codigo` INT(10) NOT NULL UNIQUE,
  `nome` VARCHAR(80) NOT NULL,
  `numCredito` INT(2) NOT NUll,
  `semestreGrade` INT(2) NOT NULL,/*01, 02, 03,...*/
  PRIMARY KEY (`idDisciplina`)
)ENGINE = InnoDB;

CREATE TABLE `SEMESTRE_DISCIPLINA` (
  `idSemestreDisciplina` INT(254) NOT NULL AUTO_INCREMENT,
  `idDisciplina` INT(10) NOT NULL,
  `horario` VARCHAR(13) NOT NULL,/*ex: 20:30 - 22:00*/
  `diasSemana` VARCHAR(20) NOT NULL,/*ex: seg-qua-qui*/
  `sala` INT(3) NOT NULL,
  `bloco` CHAR NOT NULL,
  `semestre` VARCHAR(6) NOT NULL,/*2018-1 or 2018-2*/
  PRIMARY KEY (idSemestreDisciplina),
  CONSTRAINT FK_idDisciplina1 FOREIGN KEY (idDisciplina) REFERENCES DISCIPLINA(idDisciplina)
  ON DELETE CASCADE
  ON UPDATE CASCADE
)ENGINE = InnoDB;

/*referencia a lista de alunos na class disciplina.*/
CREATE TABLE `DISCIPLINA_ALUNO` (
  `idAluCod` INT(10) NOT NULL AUTO_INCREMENT,
  `idDisciplina` INT(10) NOT NULL ,
  `idSemestreDisciplina` INT(254) NOT NULL,
  `idAluno` INT(10) NOT NULL,
  `situacao` INT(2) DEFAULT 1,
  `nota` FLOAT(4,2) DEFAULT 0.0,
  PRIMARY KEY (idAluCod),
  CONSTRAINT FK_idDisciplina2 FOREIGN KEY (idDisciplina) REFERENCES DISCIPLINA(idDisciplina)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  CONSTRAINT FK_idSemestreDisciplina FOREIGN KEY (idSemestreDisciplina) REFERENCES SEMESTRE_DISCIPLINA(idSemestreDisciplina)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  CONSTRAINT FK_idAluno2 FOREIGN KEY (idAluno) REFERENCES ALUNO(idAluno)
  ON DELETE CASCADE
  ON UPDATE CASCADE
)ENGINE = InnoDB;

CREATE TABLE `DEPENDENCIAS` (
  `idDependencia` INT(10) NOT NULL AUTO_INCREMENT,
  `idDisciplinaDependente` INT(10) NOT NULL,
  `idDisciplina` INT(10) NOT NULL,
  PRIMARY KEY (idDependencia)
)ENGINE = InnoDB;

insert into `ALUNO` (`nome`, `cpf`, `dataNascimento`, `curso`) values ('Pedro Vaz Costa Nunes', 01234567890, '08/08/08', 'CC');
insert into `LOGIN` (`usuario`, `senha`, `idAluno`) values ('aa', MD5('aa'), 1);
insert into `ALUNO` (`nome`, `cpf`, `dataNascimento`, `curso`) values ('Nelson Plinio', 0987654321, '08/08/08', 'CC');
insert into `LOGIN` (`usuario`, `senha`, `idAluno`) values ('bb', MD5('bb'), 2);

insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1000, 'Algoritmos', 60, '01');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1002, 'Fundamentos da Computação 1', 60, '01');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1004, 'Laboratório de Programação', 60, '01');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1005, 'Sistemas Digitais', 90, '01');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1006, 'Engenharia de Software', 60, '01');

insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1007, 'Engenharia de Requisitos', 60, '02');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1001, 'Técnicas de Programação 1', 60, '02');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1008, 'Fundamentos da Computação 2', 60, '02');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1003, 'Calculo 1', 90, '02');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1009, 'Geometria Analítica', 60, '02');

insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1010, 'Estrutura de Dados 1', 90, '03');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1011, 'Fundamentos da Computação 3', 60, '03');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1012, 'Técnicas de Programação 2', 60, '03');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1013, 'Língua Portuguesa 1', 60, '03');
insert into `DISCIPLINA` (`codigo`, `nome`, `numCredito`, `semestreGrade`) values (1014, 'Eletricidade e Magnetismo', 60, '03');

-- <editor-fold desc="Inserts Semestre Disciplina">
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (1, '20:30-22:00', 'seg-quin', 101, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (7, '20:30-22:00', 'ter-sex', 101, 'D', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (2, '20:30-22:00', 'ter-quar-sex', 102, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (9, '20:30-22:00', 'seg-quin', 101, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (3, '20:30-22:00', 'ter-sex', 102, 'C', '2018-2');

insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (4, '20:30-22:00', 'seg-quar-quin', 103, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (5, '20:30-22:00', 'ter-sex', 104, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (6, '20:30-22:00', 'seg-quin', 103, 'D', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (8, '20:30-22:00', 'ter-sex', 104, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (10, '20:30-22:00', 'seg-quin', 103, 'C', '2018-2');

insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (11, '20:30-22:00', 'seg-quar-quin', 105, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (12, '20:30-22:00', 'seg-quin', 201, 'C', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (13, '20:30-22:00', 'ter-sex', 201, 'D', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (14, '20:30-22:00', 'seg-quin', 103, 'D', '2018-2');
insert into `SEMESTRE_DISCIPLINA` (`idDisciplina`, `horario`, `diasSemana`, `sala`, `bloco`, `semestre`)
  values (15, '20:30-22:00', 'ter-sex', 202, 'C', '2018-2');
-- </editor-fold>

insert into `DEPENDENCIAS` (`idDisciplinaDependente`, `idDisciplina`) values (6, 5);
insert into `DEPENDENCIAS` (`idDisciplinaDependente`, `idDisciplina`) values (7, 1);
insert into `DEPENDENCIAS` (`idDisciplinaDependente`, `idDisciplina`) values (8, 2);
insert into `DEPENDENCIAS` (`idDisciplinaDependente`, `idDisciplina`) values (11, 7);
insert into `DEPENDENCIAS` (`idDisciplinaDependente`, `idDisciplina`) values (13, 7);