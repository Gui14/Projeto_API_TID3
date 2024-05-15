function mudarDiv(opcao) {
    var divPrincipal = document.getElementById('div_principal');
    divPrincipal.innerHTML = ''; // Limpa o conteúdo atual

    if (opcao === 'cadastro') {
        divPrincipal.innerHTML = '<h2>Cadastro de Usuário</h2>' +
                                 '<form action="/usuarios/cadastrar" method="POST">' +
                                 '   <label for="nome">Nome:</label>' +
                                 '   <input type="text" id="nome" name="nome">' +
                                 '   <label for="email">Email:</label>' +
                                 '   <input type="email" id="email" name="email">' +
                                 '   <label for="senha">Senha:</label>' +
                                 '   <input type="password" id="senha" name="senha">' +
                                 '   <button type="submit">Cadastrar</button>' +
                                 '</form>';
    } else if (opcao === 'visualizacao') {
        fetch('http://192.168.1.202:5000/usuarios')
        .then(response => response.json())
        .then(data => {
          var usuariosHTML = '<h2>Visualização de Usuários</h2>' +
                             '<table>' +
                             '   <tr><th>Nome</th><th>Email</th></tr>';
          data.forEach(usuario => {
              usuariosHTML += '<tr><td>' + usuario.nome + '</td><td>' + usuario.email + '</td></tr>';
          });
          usuariosHTML += '</table>';
          divPrincipal.innerHTML = usuariosHTML;
        })
        .catch(error => {
          console.error('Erro ao obter usuários:', error);
        });
    } else if (opcao === 'agendamentos') {
        fetch('http://192.168.1.202:5000/agendamento')
          .then(response => response.json())
          .then(data => {
            var agendamentosHTML = '<h2>Visualização de Agendamento</h2>' +
                                   '<table>' +
                                   '   <tr><th>Data</th><th>Horário</th><th>Nome</th><th>Hemocentro</th><th>Status</th><th>Ações</th></tr>';
            data.forEach(agendamento => {
                agendamentosHTML += '<tr>' +
                                    '<td>' + agendamento.data_agendamento + '</td>' +
                                    '<td>' + agendamento.horario_agendamento + '</td>' +
                                    '<td>' + agendamento.nome_doador + '</td>' +
                                    '<td>' + agendamento.hemocentro + '</td>' +
                                    '<td>' + agendamento.status + '</td>' +
                                    '<td><button onclick="atualizarStatus(' + agendamento.id_agendamento + ')">Concluir</button></td>' +
                                    '<td><button onclick="atualizarCancelar(' + agendamento.id_agendamento + ')">Cancelar</button></td>' +
                                    '</tr>';
            });
            agendamentosHTML += '</table>';
            divPrincipal.innerHTML = agendamentosHTML;
          })
          .catch(error => {
            console.error('Erro ao obter agendamentos:', error);
          });
    }
}

function atualizarStatus(id_agendamento) {
    fetch('http://192.168.1.202:5000/agendamento/atualizar/' + id_agendamento, {
        method: 'PUT',
    })
    .then(response => {
        if (response.ok) {
            console.log('Status atualizado com sucesso!');
            // Recarregar a visualização de agendamentos
            mudarDiv('agendamentos');
        } else {
            console.error('Falha ao atualizar o status do agendamento:', response.status);
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar o status do agendamento:', error);
    });
}

function atualizarCancelar(id_agendamento) {
    fetch('http://192.168.1.202:5000/agendamento/cancelar/' + id_agendamento, {
        method: 'PUT',
    })
    .then(response => {
        if (response.ok) {
            console.log('Status atualizado com sucesso!');
            // Recarregar a visualização de agendamentos
            mudarDiv('agendamentos');
        } else {
            console.error('Falha ao atualizar o status do agendamento:', response.status);
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar o status do agendamento:', error);
    });
}