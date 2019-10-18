from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('name', 50)
            table.string('last_name', 50)
            table.integer('age')
            table.char('gender', 1)
            table.integer('status')
            table.nullable_timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
