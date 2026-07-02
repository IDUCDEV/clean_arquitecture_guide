### 5.3 Presentation Layer (El Mesero)

#### States

**Archivo**: `lib/features/user/presentation/cubit/user_state.dart`

```dart
part of 'user_cubit.dart';

abstract class UserState extends Equatable {
  const UserState();
  
  @override
  List<Object?> get props => [];
}

class UserInitial extends UserState {}
class UserLoading extends UserState {}

class UsersLoaded extends UserState {
  final List<User> users;
  const UsersLoaded(this.users);
  
  @override
  List<Object?> get props => [users];
}

class UserLoaded extends UserState {
  final User user;
  const UserLoaded(this.user);
  
  @override
  List<Object?> get props => [user];
}

class UserError extends UserState {
  final String message;
  const UserError(this.message);
  
  @override
  List<Object?> get props => [message];
}

class UserOperationSuccess extends UserState {
  final String message;
  const UserOperationSuccess(this.message);
  
  @override
  List<Object?> get props => [message];
}
```

#### Cubit

**Archivo**: `lib/features/user/presentation/cubit/user_cubit.dart`

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/usecases/create_user.dart';
import 'package:my_app/features/user/domain/usecases/delete_user.dart';
import 'package:my_app/features/user/domain/usecases/get_user.dart';
import 'package:my_app/features/user/domain/usecases/get_users.dart';

part 'user_state.dart';

class UserCubit extends Cubit<UserState> {
  final GetUsers _getUsers;
  final GetUser _getUser;
  final CreateUser _createUser;
  final DeleteUser _deleteUser;
  
  UserCubit({
    required GetUsers getUsers,
    required GetUser getUser,
    required CreateUser createUser,
    required DeleteUser deleteUser,
  })  : _getUsers = getUsers,
        _getUser = getUser,
        _createUser = createUser,
        _deleteUser = deleteUser,
        super(UserInitial());
  
  Future<void> loadUsers() async {
    emit(UserLoading());
    
    final result = await _getUsers(NoParams());
    
    result.match(
      (failure) => emit(UserError(failure.toString())),
      (users) => emit(UsersLoaded(users)),
    );
  }
  
  Future<void> loadUser(String id) async {
    emit(UserLoading());
    
    final result = await _getUser(GetUserParams(id));
    
    result.match(
      (failure) => emit(UserError(failure.toString())),
      (user) => emit(UserLoaded(user)),
    );
  }
  
  Future<void> createUser(String name, String email) async {
    emit(UserLoading());
    
    final result = await _createUser(
      CreateUserParams(name: name, email: email),
    );
    
    result.match(
      (failure) => emit(UserError(failure.toString())),
      (_) {
        emit(const UserOperationSuccess('User created'));
        loadUsers();
      },
    );
  }
  
  Future<void> deleteUser(String userId) async {
    emit(UserLoading());
    
    final result = await _deleteUser(DeleteUserParams(userId));
    
    result.match(
      (failure) => emit(UserError(failure.toString())),
      (_) {
        emit(const UserOperationSuccess('User deleted'));
        loadUsers();
      },
    );
  }
}
```

---

> 📖 **Para una guía completa de BLoC/Cubit** (widgets, concurrencia, hydrated, testing, buenas prácticas, proyecto integrador): módulo [`16-BLOC-CUBIT/`](../16-BLOC-CUBIT/).

### 5.4 UI Layer (El Cliente)

#### Users List Page

**Archivo**: `lib/features/user/presentation/pages/users_list_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/user/presentation/cubit/user_cubit.dart';

class UsersListPage extends StatelessWidget {
  const UsersListPage({super.key});
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<UserCubit>()..loadUsers(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Users')),
        body: const _UsersListView(),
        floatingActionButton: FloatingActionButton(
          onPressed: () => _showCreateDialog(context),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
  
  void _showCreateDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (dialogContext) => BlocProvider.value(
        value: context.read<UserCubit>(),
        child: const _CreateUserDialog(),
      ),
    );
  }
}

class _UsersListView extends StatelessWidget {
  const _UsersListView();
  
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<UserCubit, UserState>(
      listener: (context, state) {
        if (state is UserOperationSuccess) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        if (state is UserLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        
        if (state is UsersLoaded) {
          if (state.users.isEmpty) {
            return const Center(child: Text('No users yet'));
          }
          
          return ListView.builder(
            itemCount: state.users.length,
            itemBuilder: (context, index) {
              final user = state.users[index];
              return ListTile(
                leading: CircleAvatar(
                  child: Text(user.name[0].toUpperCase()),
                ),
                title: Text(user.name),
                subtitle: Text(user.email),
                trailing: IconButton(
                  icon: const Icon(Icons.delete, color: Colors.red),
                  onPressed: () => _confirmDelete(context, user.id),
                ),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => BlocProvider.value(
                      value: context.read<UserCubit>(),
                      child: UserDetailPage(userId: user.id),
                    ),
                  ),
                ),
              );
            },
          );
        }
        
        if (state is UserError) {
          return Center(child: Text(state.message));
        }
        
        return const SizedBox.shrink();
      },
    );
  }
  
  void _confirmDelete(BuildContext context, String userId) {
    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Delete User'),
        content: const Text('Are you sure you want to delete this user?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              context.read<UserCubit>().deleteUser(userId);
            },
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}

class _CreateUserDialog extends StatefulWidget {
  const _CreateUserDialog();

  @override
  State<_CreateUserDialog> createState() => _CreateUserDialogState();
}

class _CreateUserDialogState extends State<_CreateUserDialog> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('New User'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Name'),
          ),
          TextField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
            keyboardType: TextInputType.emailAddress,
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancel'),
        ),
        TextButton(
          onPressed: () {
            final name = _nameController.text;
            final email = _emailController.text;
            if (name.isNotEmpty && email.isNotEmpty) {
              context.read<UserCubit>().createUser(name, email);
              Navigator.pop(context);
            }
          },
          child: const Text('Create'),
        ),
      ],
    );
  }
}
```

#### User Detail Page

**Archivo**: `lib/features/user/presentation/pages/user_detail_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/user/presentation/cubit/user_cubit.dart';

class UserDetailPage extends StatelessWidget {
  final String userId;
  
  const UserDetailPage({super.key, required this.userId});
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<UserCubit>()..loadUser(userId),
      child: Scaffold(
        appBar: AppBar(title: const Text('User Details')),
        body: const _UserDetailView(),
      ),
    );
  }
}

class _UserDetailView extends StatelessWidget {
  const _UserDetailView();

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<UserCubit, UserState>(
      builder: (context, state) {
        if (state is UserLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        
        if (state is UserLoaded) {
          final user = state.user;
          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: CircleAvatar(
                    radius: 50,
                    child: Text(
                      user.name[0].toUpperCase(),
                      style: const TextStyle(fontSize: 40),
                    ),
                  ),
                ),
                const SizedBox(height: 24),
                _DetailRow(label: 'Name', value: user.name),
                _DetailRow(label: 'Email', value: user.email),
                _DetailRow(
                  label: 'Active', 
                  value: user.isActive ? 'Yes' : 'No',
                ),
                if (user.createdAt != null)
                  _DetailRow(
                    label: 'Created', 
                    value: user.createdAt!.toString().split(' ')[0],
                  ),
                if (user.isNew)
                  const Chip(
                    label: Text('NEW'),
                    backgroundColor: Colors.green,
                  ),
              ],
            ),
          );
        }
        
        if (state is UserError) {
          return Center(child: Text(state.message));
        }
        
        return const SizedBox.shrink();
      },
    );
  }
}

class _DetailRow extends StatelessWidget {
  final String label;
  final String value;

  const _DetailRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}
```

---
