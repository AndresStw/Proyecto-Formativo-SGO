
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class Inventario(Base):
    __tablename__ = "inventarios"

    idInventario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador del inventario"
    )

    stockActual: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Cantidad actual de insumos"
    )

    stockMinimo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Cantidad mínima permitida"
    )

    idAdministrador: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("administradores.idAdministrador"),
        nullable=False,
        comment="Administrador responsable del inventario"
    )

    administrador: Mapped["Administrador"] = relationship(
        "Administrador",
        back_populates="inventarios"
    )

    insumos: Mapped[list["Insumo"]] = relationship(
        "Insumo",
        back_populates="inventario"
    )


class Insumo(Base):
    __tablename__ = "insumos"

    idInsumo: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador del insumo"
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nombre del insumo"
    )

    unidadMedida: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Unidad de medida del insumo"
    )

    idInventario: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("inventarios.idInventario"),
        nullable=False,
        comment="Inventario al que pertenece el insumo"
    )

    inventario: Mapped["Inventario"] = relationship(
        "Inventario",
        back_populates="insumos"
    )

    detallesReceta: Mapped[list["DetalleReceta"]] = relationship(
        "DetalleReceta",
        back_populates="insumo"
    )


class Receta(Base):
    __tablename__ = "recetas"

    idReceta: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador de la receta"
    )

    descripcion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Descripción de la receta"
    )

    idPlato: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("plato.idPlato"),
        unique=True,
        nullable=False,
        comment="Plato al que pertenece la receta"
    )

    plato: Mapped["Plato"] = relationship(
        "Plato",
        back_populates="receta"
    )

    detalles: Mapped[list["DetalleReceta"]] = relationship(
        "DetalleReceta",
        back_populates="receta",
        cascade="all, delete-orphan"
    )


class DetalleReceta(Base):
    __tablename__ = "detalleRecetas"

    idDetalleReceta: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador del detalle de receta"
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Cantidad de insumo necesaria para la receta"
    )

    idReceta: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("recetas.idReceta"),
        nullable=False,
        comment="Receta a la que pertenece el detalle"
    )

    idInsumo: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("insumos.idInsumo"),
        nullable=False,
        comment="Insumo utilizado en la receta"
    )

    receta: Mapped["Receta"] = relationship(
        "Receta",
        back_populates="detalles"
    )

    insumo: Mapped["Insumo"] = relationship(
        "Insumo",
        back_populates="detallesReceta"
    )
